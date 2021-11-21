from fastapi import FastAPI

# from passlib.utils.decor import deprecated_method
from sqlalchemy import engine
# from sqlalchemy.orm.session import Session
# from sqlalchemy.sql.functions import mode
# from starlette import requests
from . import models
from .database import engine, get_db
from .routers import baselines, profiles, systems

models.Base.metadata.create_all(bind=engine)

api = FastAPI(title="SysProfileAPI", version="0.6.0")

api.include_router(baselines.router)
api.include_router(profiles.router)
api.include_router(systems.router)


@api.get("/")
async def root():
    return {"messaage":"Welcome to " + api.title + " " + api.version}
