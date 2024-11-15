from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    
    First_Name : str
    Last_Name : str
    Department : str
    Address : str
    Email : str
    username : str
    password : str
    
class UpdateUserRequest(BaseModel):
    First_Name : str
    Last_Name : str
    Department : str
    Address : str
    Email : str
    username : str
    password : str