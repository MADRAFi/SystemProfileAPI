from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from starlette.routing import Router
from api import models, schemas
from api.database import engine, get_db
from sqlalchemy import engine
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import mode

router = APIRouter()

#######################################################################################################################
# OS Systems
#######################################################################################################################

@router.get("/os_systems")
def get_systems(db: Session = Depends(get_db)):

    systems = db.query(models.SystemOS).all()
    return { "data": systems}