from pydantic import BaseModel, EmailStr

class CreateTenantRequest(BaseModel):
    tenantname : str
    email : EmailStr
    password : str
    
class UpdateTenantRequest(BaseModel):
    new_tenantname: str
    
    