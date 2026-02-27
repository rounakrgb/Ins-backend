#import pdb; pdb.set_trace()

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import bcrypt
from pydantic import BaseModel

from database import engine, get_db
from model import Base, User, Profile
from jwt_token import create_access_token, decode_jwt_token


class SignupRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class Item(BaseModel):
    name:str
    des: str = None
    price:float
    
class ProfileUpdate(BaseModel):
    bio:str
    age:int    

app = FastAPI()
security = HTTPBearer(auto_error=False)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "API Running 🚀"}


@app.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = bcrypt.hashpw(
        request.password.encode("utf-8"),
        bcrypt.gensalt()
    )

    user = User(
        username=request.username,
        password=hashed_password.decode("utf-8")
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created successfully"}

@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == request.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not bcrypt.checkpw(
        request.password.encode("utf-8"),
        user.password.encode("utf-8")
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Missing credentials")
    
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    
    try:
        payload = decode_jwt_token(token)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token decode error: {str(e)}")
    
    print(f"Decoded payload: {payload}")
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token: no user id")

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=401, detail=f"User not found for id: {user_id}")

    return user 
    


@app.get("/users")
def get_all_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return {
        "id": current_user.id,
        "username": current_user.username,
        "profile": current_user.profile
    }
    
    
@app.put("/profile")
def update_profile(
    data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # look for an existing profile; if none, create one linking it to the current user
    profile = db.query(Profile).filter(
        Profile.user_id == current_user.id
    ).first()

    if profile is None:
        profile = Profile(user_id=current_user.id)
        db.add(profile)
    
    profile.bio = data.bio
    profile.age = data.age

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return {"message": "Profile saved successfully"}



# @app.get("/Name")
# def show_name(name:str):
#     return {"message": name}
    
# @app.get("/Name/{name}")
# def show_name_by_path(name):
#     return {"msg":name}    

# @app.post("/items/")
# def create_items(item: Item):
#     return item
