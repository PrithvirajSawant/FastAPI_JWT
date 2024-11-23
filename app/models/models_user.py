from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import relationship




class Users(Base):
    __tablename__ = "users"
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)  # Foreign key referencing "tenants"
    id=Column(Integer,primary_key=True,index=True)
    First_Name = Column(String(100), nullable=False)
    Last_Name = Column(String(100), nullable=False) 
    Department = Column(String(100), nullable = False)
    Address = Column(String(100), nullable=False)
    Email =  Column(EmailType, nullable=False, unique=True)
    username=Column(String(100), unique=True)
    hashed_password = Column(String(100))
    # email=Column(String(100),unique=True)
    # password=Column(String())
    
    # Define a relationship if needed, for example:
    tenant = relationship("Tenants", back_populates="user")
