from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from api import models, schemas
from api.database import engine, get_db
from sqlalchemy import engine
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import mode

router = APIRouter(
    prefix= "/systems",
    tags=['Systems']
)
#######################################################################################################################
# OS Systems
#######################################################################################################################

@router.get("/")
def get_systems(db: Session = Depends(get_db)):

    systems = db.query(models.SystemOS).all()
    # return { "data": systems}
    return systems