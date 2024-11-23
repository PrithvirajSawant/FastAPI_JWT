from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from sqlalchemy.orm import Session
from starlette import status

from app.models.models_user import Users
from passlib.context import CryptContext

from jose import jwt, JWTError

#importing the dto class
from app.schemas.user_token_schema import Token

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
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
    user = authenticate_user(form_data.username , form_data.password, db) #fun.  | username is predefined
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    
    #tenant_id = user.tenant_id
    
    # if not user or user.username != "Admin": #generating token for admin-only
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized: Only 'Admin' is allowed to log in.")
    
    token = create_access_token(user_name=user.username, user_id=user.id,tenant_id=user.tenant_id, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) #fun.  | username over here is w.r.to models.py
    
    return {"access_token":token, "token_type":"bearer"}
    
def authenticate_user(userName: str, password: str, db):
    user = db.query(Users).filter(Users.username == userName).first() # | username over here is w.r.to models.py
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(user_name:str, user_id: int, tenant_id:int, expires_delta: timedelta):
    encode = {'sub' : user_name, 'id' : user_id,  'exp': (datetime.now(timezone.utc) + expires_delta).timestamp()  # Expiration time
}
    #expires = datetime.now(timezone.utc) + expires_delta
    #encode['exp'] = expires.timestamp()
    #encode.update({'exp':expires})
    print("Token payload before encoding:", encode)  # Debugging log
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Decoding the token
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    # credentials_exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Could not validate user",
    #     headers={"WWW-Authenticate": "Bearer"}
    # )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Decoded payload:", payload)  # Debugging log
        user_name : str = payload.get('sub')
        user_id : int = payload.get('id')
        #tenant_id : int = payload.get('tenant_id')
        if not all([user_name, user_id]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is missing required claims (username, user_id, tenant__id).')
            #raise credentials_exception
        #EXAMPLE FOR Restricting PARTICULAR TENANT
        # if user_name == 'Aryan' or tenant_id == 1:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User - Aryan is not AuthZ.')
        
        # if user_name != "Aryan":
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this resource.")
        
        if 'exp' not in payload or payload['exp'] < datetime.now(timezone.utc).timestamp():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token has expired.')
            #raise credentials_exception
        return {'username': user_name, 'user_id': user_id}
    except JWTError as e:
        print("JWTError:", str(e))  # Debugging log
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
        #raise credentials_exception
        
        
###################################################################################################################### fetching the tenant_id from the incoming request

async def extract_tenant_id_from_token(request: Request):
    # Get the token from the Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    token = auth_header.split(" ")[1]  # Extract token
    try:
        payload = jwt.decode(token, "YOUR_SECRET_KEY", algorithms=["HS256"])
        tenant_id = payload.get("tenant_id")
        if not tenant_id:
            raise HTTPException(status_code=400, detail="Tenant ID not found in token")
        return tenant_id
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")