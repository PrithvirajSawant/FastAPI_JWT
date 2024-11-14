from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from sqlalchemy.orm import Session
from starlette import status

from app.models.models import Users
from passlib.context import CryptContext

from jose import jwt, JWTError

#importing the dto class
from app.schemas.token_schema import Token

#importing from database
from app.database.user_database import get_db

# importing files from .env
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix = '/auth',
    tags = ['auth']
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

db_dependency = Annotated[Session, Depends(get_db)]

# AuthN
# todo : remove the endpoint (make it a function)
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db:db_dependency):
    user = authenticate_user(form_data.username , form_data.password, db) #fun.  | username is predefined
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    
    # if not user or user.username != "Admin": #generating token for admin-only
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized: Only 'Admin' is allowed to log in.")
    
    token = create_access_token(user.username, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) #fun.  | username over here is w.r.to models.py
    
    return {"access_token":token, "token_type":"bearer"}
    
def authenticate_user(userName: str, password: str, db):
    user = db.query(Users).filter(Users.username == userName).first() # | username over here is w.r.to models.py
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(user_name:str, user_id: int, expires_delta: timedelta):
    encode = {'sub' : user_name, 'id' : user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode['exp'] = expires.timestamp()
    # encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Decoding the token
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name : str = payload.get('sub')
        user_id : int = payload.get('id')
        if user_name is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user as its NULL.')
        #EXAMPLE FOR Restricting PARTICULAR TENANT
        # if user_name == 'Aryan' or tenant_id == 1:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User - Aryan is not AuthZ.')
        
        # if user_name != "Aryan":
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this resource.")
        
        if 'exp' not in payload or payload['exp'] < datetime.now(timezone.utc).timestamp():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token has expired.')
        return {'username': user_name, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')