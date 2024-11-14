from fastapi import Depends, HTTPException, Request, status
from typing import Annotated
from sqlalchemy.orm import Session

#importing the database package
from app.database.user_database import get_db
from app.models.models_user import Users
import app.models.models_user as User

#importing the dto package
from app.schemas.user_schema import CreateUserRequest
from app.schemas.user_schema import UpdateUserRequest

#importing the auth package
from app.auth.auth_user import get_current_user
from app.auth.auth_user import pwd_context

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]



async def create_user(user: user_dependency, db:db_dependency, create_user_request: CreateUserRequest):
    
    if user["username"] != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Only 'Admin' can view all users.")
    
    create_user_model = Users(
        username = create_user_request.username,
        hashed_password = pwd_context.hash(create_user_request.password)
    )
    db.add(create_user_model)
    db.commit()
    return {"msg": f"User added successfully"}

# //////////////////////////

async def fetch_all_users(user: user_dependency, db : db_dependency):

    if user["username"] != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Only 'Admin' can view all users.")
    
    users = db.query(Users).all()

    return {"users": [{"id": t.id, "username": t.username} for t in users]}

# //////////////////////////

async def update_user_name(user_id : int ,user: user_dependency, db: db_dependency, update_request: UpdateUserRequest):
    # Fetch the current tenant from the database
    if user["username"] != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied [Only Admin is AuthZ]")
    
    db_user = db.query(Users).filter(Users.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db_user.username = update_request.new_username
    db.commit()
    db.refresh(db_user)
    return {"msg": f"User {user_id} name updated successfully", "new_username": db_user.username}

# //////////////////////////

async def delete_user(user_id: int, user : user_dependency, db : db_dependency):

    if user["username"] != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied [Only Admin is AuthZ]")
    
    db_user = db.query(Users).filter(Users.id == user_id).first()
    
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to delete")
    
    db.delete(db_user)
    db.commit()
    return{"detail" : f"User {user_id} deleted successfully"}