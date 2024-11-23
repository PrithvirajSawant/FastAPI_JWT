# from app.database.tenant_database import Base
# from sqlalchemy import Column, Integer, String

# class Tenants(Base):
#     __tablename__ = "tenants"
#     id=Column(Integer,primary_key=True,index=True)
#     email = Column(String)
#     tenantname=Column(String(100), unique=True)
#     hashed_password = Column(String(100))
#     # email=Column(String(100),unique=True)
#     # password=Column(String())

    
from app.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import relationship



class Tenants(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenantname = Column(String(255), nullable=False)  # "name" field
    email = Column(EmailType, nullable = False)
    created_at = Column(TIMESTAMP, server_default=func.now())  # Default to current timestamp
    hashed_password = Column(String(100))
    
    # Establish relationship
    user = relationship("Users", back_populates="tenant")

