from app.database.tenant_database import Base
from sqlalchemy import Column, Integer, String

class Tenants(Base):
    __tablename__ = "tenants"
    id=Column(Integer,primary_key=True,index=True)
    tenantname=Column(String(100), unique=True)
    hashed_password = Column(String(100))
    # email=Column(String(100),unique=True)
    # password=Column(String())