from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from sqlalchemy.orm import Session
from starlette import status

from app.models.models_tenant import Tenants
from passlib.context import CryptContext

from jose import jwt, JWTError

#importing the dto class
from app.schemas.tenant_token_schema import Token

#importing from database
from app.database.tenant_database import get_db

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
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db:db_dependency):
    tenant = authenticate_tenant(form_data.username , form_data.password, db) #fun.  | username is predefined
    if not tenant:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate tenant")
    
    # if not tenant or tenant.tenantname != "Admin": #generating token for admin-only
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized: Only 'Admin' is allowed to log in.")
    
    token = create_access_token(tenant.tenantname, tenant.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) #fun.  | tenantname over here is w.r.to models.py
    
    return {"access_token":token, "token_type":"bearer"}
    
def authenticate_tenant(tenantname: str, password: str, db):
    tenant = db.query(Tenants).filter(Tenants.tenantname == tenantname).first() # | tenantname over here is w.r.to models.py
    if not tenant:
        return False
    if not pwd_context.verify(password, tenant.hashed_password):
        return False
    return tenant

def create_access_token(tenant_name:str, tenant_id: int, expires_delta: timedelta):
    encode = {'sub' : tenant_name, 'id' : tenant_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode['exp'] = expires.timestamp()
    print("Token payload before encoding:", encode)  # Debugging line
    # encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Decoding the token
async def get_current_tenant(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        tenant_name : str = payload.get('sub')
        tenant_id : int = payload.get('id')
        if tenant_name is None or tenant_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate tenant as its NULL.')
        #EXAMPLE FOR Restricting PARTICULAR TENANT
        # if tenant_name == 'Aryan' or tenant_id == 1:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='TENANT - Aryan is not AuthZ.')
        
        # if tenant_name != "Aryan":
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this resource.")
        
        if 'exp' not in payload or payload['exp'] < datetime.now(timezone.utc).timestamp():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token has expired.')
        return {'tenantname': tenant_name, 'id': tenant_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate tenant.')