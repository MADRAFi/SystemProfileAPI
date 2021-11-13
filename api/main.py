from  fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body, Depends
from pydantic import BaseModel

from sqlalchemy import engine
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import mode
from starlette import requests
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

api = FastAPI(title="SysProfAPI", version="0.1.0")

class ProfileBase(BaseModel):
    name: str
    fqdn: str
    ip: str
    netmask: str
    gateway: str

class ProfileCreate(ProfileBase):
    pass


@api.get("/")
async def root():
    return {"messaage":"Welcome to Profile API"}

@api.get("/profiles")
def get_profiles(db: Session = Depends(get_db)):

    profiles = db.query(models.Profile).all()
    return { "data": profiles}

@api.post("/profiles", status_code=status.HTTP_201_CREATED)
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    new_profile = models.Profile(**profile.dict())
    try:
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        return {"data": new_profile}
    except Exception as error:
        print("Error:", error.__cause__)
        return {"data": str(error.__cause__)}

@api.get("/profiles/{server_name}")
def get_profile(server_name: str, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.name == server_name).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Profile for server {server_name} was not found")
    return { "profile" : profile}

@api.delete("/profiles/{server_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(server_name: str, db: Session = Depends(get_db)):
    profileq = db.query(models.Profile).filter(models.Profile.name == server_name)
    profile = profileq.first()
    if profile == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Profile for server {server_name} does not exists")
    else:
        profileq.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

@api.put("/profiles/{server_name}")
def update_profile(server_name: str, profile: ProfileCreate, db: Session = Depends(get_db)):
    profileq = db.query(models.Profile).filter(models.Profile.name == server_name)
    existing_profile = profileq.first()
    if existing_profile == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Profile for server {server_name} does not exists")
    else:
        profileq.update(profile.dict(), synchronize_session=False)
        db.commit()
        return { "profile" : profileq.first()}
