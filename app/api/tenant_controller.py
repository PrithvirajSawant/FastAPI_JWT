from fastapi import status, APIRouter, Depends

#importing the dto class
from app.schemas.tenant_tenant_schema import CreateTenantRequest
from app.schemas.tenant_tenant_schema import UpdateTenantRequest

#importing dao package
from app.database.dao import tenant_dao

from app.database.dao.tenant_dao import db_dependency
from app.database.dao.tenant_dao import tenant_dependency


# I have used modular approach for organization
router = APIRouter()



@router.post("/create-tenants",status_code=status.HTTP_201_CREATED)
async def create_tenant( tenant: tenant_dependency,db:db_dependency, create_tenant_request: CreateTenantRequest):
    return await tenant_dao.create_tenant( tenant, db, create_tenant_request)

@router.get("/view-all-tenants", status_code=status.HTTP_200_OK)
async def view_all_tenants(tenant: tenant_dependency, db: db_dependency):
    return await tenant_dao.fetch_all_tenants(tenant,db)

@router.put("/update_tenant_name", status_code=status.HTTP_200_OK)
async def update_tenant_name(tenant_id : int ,tenant: tenant_dependency, db: db_dependency, update_request: UpdateTenantRequest):
    return await tenant_dao.update_tenant_name(tenant_id,tenant,db,update_request)

@router.delete("/delete_tenant/{tenant_id}", status_code=status.HTTP_200_OK)
async def delete_tenant(tenant_id: int, tenant : tenant_dependency, db : db_dependency):
    return await tenant_dao.delete_tenant(tenant_id,tenant,db)