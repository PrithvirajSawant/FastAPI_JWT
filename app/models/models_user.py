from app.database.user_database import Base
from sqlalchemy import Column, Integer, String

class Users(Base):
    __tablename__ = "users"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String(100), unique=True)
    hashed_password = Column(String(100))
    # email=Column(String(100),unique=True)
    # password=Column(String())