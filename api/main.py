from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body, Depends

from passlib.utils.decor import deprecated_function, deprecated_method
from sqlalchemy import engine
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import mode
from starlette import requests
from api import models, schemas, functions
from api.database import engine, get_db
from api.routers import baselines, profiles, systems

models.Base.metadata.create_all(bind=engine)

api = FastAPI(title="SysProfileAPI", version="0.3.0")

api.include_router(baselines.router)
api.include_router(profiles.router)
api.include_router(systems.router)

@api.get("/")
async def root():
    return {"messaage":"Welcome to SysProfile API"}
