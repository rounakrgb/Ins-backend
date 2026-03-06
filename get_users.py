from redis_client import redis_client

@app.get("/users/{user_id}")
def get_user(user_id: int):
    cached_user = redis_client.get(f"user:{user_id}")
    
    
    if cached_user:
        return {"data": cached_user, "source":"cache"}
    
    user = db.query(User).filter(User_id == user_id).first()
    redis_client.set("f{user_id}", str(user.username),ex = 60)
    return {"data":user.username, "source":"database"}
