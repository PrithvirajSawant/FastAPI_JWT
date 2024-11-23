# from fastapi import FastAPI
# from app.auth import auth_tenant, auth_user 
# from app.api import tenant_controller, user_controller
# from app.models import models_tenant, models_user
# from app.database.tenant_database import engine

# from app.database.user_database import engine
# from app.middleware.middleware import AdvMiddleware


# app = FastAPI()

# app.add_middleware(AdvMiddleware)

# app.include_router(auth_tenant.router)
# app.include_router(auth_user.router)
# app.include_router(tenant_controller.router)
# app.include_router(user_controller.router)


# models_tenant.Base.metadata.create_all(bind=engine)
# models_user.Base.metadata.create_all(bind=engine)



from fastapi import FastAPI
from app.auth import auth_tenant, auth_user
from app.api import tenant_controller, user_controller
from app.models import models_tenant, models_user
#from app.database.tenant_database import engine as tenant_engine
#from app.database.user_database import engine as user_engine
from app.database import engine
from app.middleware.middleware import AdvMiddleware

app = FastAPI()

# Add middleware
app.add_middleware(AdvMiddleware)

# Include routers
app.include_router(auth_tenant.router)
app.include_router(auth_user.router)
app.include_router(tenant_controller.router)
app.include_router(user_controller.router)

# Create tables for both models
models_tenant.Base.metadata.create_all(bind=engine)
models_user.Base.metadata.create_all(bind=engine)
