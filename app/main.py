from fastapi import FastAPI
from app.auth import auth_user
from app.api import user_controller
from app.models import models_user
from app.database.user_database import engine
from app.middleware.middleware import AdvMiddleware


app = FastAPI()

app.add_middleware(AdvMiddleware)

app.include_router(auth_user.router)
app.include_router(user_controller.router)

models_user.Base.metadata.create_all(bind=engine)
