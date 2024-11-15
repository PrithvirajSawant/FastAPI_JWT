from pydantic import BaseModel

class CreateTenantRequest(BaseModel):
    tenantname : str
    password : str
    
class UpdateTenantRequest(BaseModel):
    new_tenantname: str