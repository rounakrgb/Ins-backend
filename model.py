from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

    profile = relationship("Profile", back_populates="user", uselist=False)
    

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    bio = Column(String)
    age = Column(Integer)

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="profile")