from fastapi import status, APIRouter

#importing the dto class
from app.schemas.user_user_schema import CreateUserRequest
from app.schemas.user_user_schema import UpdateUserRequest

#importing dao package
from app.database.dao import user_dao

from app.database.dao.user_dao import db_dependency
from app.database.dao.user_dao import user_dependency


# I have used modular approach for organization
router = APIRouter()

@router.post("/create-users",status_code=status.HTTP_201_CREATED)
async def create_user(user: user_dependency, db:db_dependency, create_user_request: CreateUserRequest):
    return await user_dao.create_user(user, db, create_user_request)

@router.get("/view-all-users", status_code=status.HTTP_200_OK)
async def view_all_users(user: user_dependency, db: db_dependency):
    return await user_dao.fetch_all_users(user,db)

@router.put("/update_user_name", status_code=status.HTTP_200_OK)
async def update_user_name(user_id : int ,user: user_dependency, db: db_dependency, update_request: UpdateUserRequest):
    return await user_dao.update_user_name(user_id,user,db,update_request)

@router.delete("/delete_user/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, user : user_dependency, db : db_dependency):
    return await user_dao.delete_user(user_id,user,db)