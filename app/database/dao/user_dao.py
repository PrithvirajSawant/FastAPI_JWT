from fastapi import Depends, HTTPException, Request, status
from typing import Annotated
from sqlalchemy.orm import Session

#importing the database package
from app.auth.auth_tenant import get_current_tenant
from app.database.user_database import get_db
from app.models.models_user import Users
import app.models.models_user as User

#importing the dto package
from app.schemas.user_user_schema import CreateUserRequest
from app.schemas.user_user_schema import UpdateUserRequest

#importing the auth package
from app.auth.auth_user import get_current_user
from app.auth.auth_user import pwd_context

#from app.auth.auth_tenant import get_current_tenant

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
# The line `#tenant_dependency = Annotated[dict, Depends(get_current_tenant)]` is a commented-out line
# of code in the provided Python script. It appears to be defining a dependency for handling the
# current tenant in the FastAPI application.
tenant_dependency = Annotated[dict, Depends(get_current_tenant)]



async def create_user(tenant: tenant_dependency, db:db_dependency, create_user_request: CreateUserRequest):
    
    if tenant["tenantname"] != "Tenant3":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Only 'Admin' can view all users.")
    
    t_id = tenant.get("id")
    if t_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant ID is required."
        )    
    create_user_model = Users(
        tenant_id = t_id,
        First_Name=create_user_request.First_Name,
        Last_Name=create_user_request.Last_Name,
        Department = create_user_request.Department,
        Address=create_user_request.Address,
        Email = create_user_request.Email,
        username = create_user_request.username,
        hashed_password = pwd_context.hash(create_user_request.password)
        
    )
    db.add(create_user_model)
    db.commit()
    return {"msg": f"User added successfully"}

# //////////////////////////

async def fetch_all_users(user: user_dependency, db : db_dependency):

    if user["username"] != "vikas":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Only 'Admin' can view all users.")
    
    users = db.query(Users).all()

    return {"users": [{"id": t.id, "username": t.username} for t in users]}

# //////////////////////////

async def update_user_name(user_id : int ,user: user_dependency, db: db_dependency, update_request: UpdateUserRequest):
    # Fetch the current tenant from the database
    if user["username"] != "vikas":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied [Only Admin is AuthZ]")
    
    db_user = db.query(Users).filter(Users.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # fields to update
    db_user.create_user_model = Users()
    db_user.First_Name=update_request.First_Name
    db_user.Last_Name=update_request.Last_Name
    db_user.Department = update_request.Department
    db_user.Address=update_request.Address
    db_user.Email = update_request.Email
    db_user.username = update_request.username
    db_user.hashed_password = pwd_context.hash(update_request.password)
    
    db.commit()
    db.refresh(db_user)
    return {"msg": f"User {user_id} name updated successfully"}

# //////////////////////////

async def delete_user(user_id: int, user : user_dependency, db : db_dependency):

    if user["username"] != "vikas":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied [Only Admin is AuthZ]")
    
    db_user = db.query(Users).filter(Users.id == user_id).first()
    
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to delete")
    
    db.delete(db_user)
    db.commit()
    return{"detail" : f"User {user_id} deleted successfully"}