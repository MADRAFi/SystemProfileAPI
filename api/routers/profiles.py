from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from api import models, schemas
from api.database import engine, get_db
from sqlalchemy import engine
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import mode


router = APIRouter(
    prefix= "/profiles"
)

#######################################################################################################################
# Profiles
#######################################################################################################################

@router.get("/")
def get_profiles(db: Session = Depends(get_db)):

    profiles = db.query(models.Profile).all()
    return profiles

@router.post("/", status_code=status.HTTP_201_CREATED)
# def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
def create_profile(profile: schemas.ProfileBase, db: Session = Depends(get_db)):


    # password_hash = functions.hash_password(profile.password)
    # profile.password = password_hash
    new_profile = models.Profile(**profile.dict())

    try:
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        # return {"data": new_profile}
        return new_profile
    except Exception as error:
        print("Error:", error.__cause__)
        # return {"data": str(error.__cause__)}
        return str(error.__cause__)

@router.get("/{server_name}")
def get_profile(server_name: str, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.name == server_name).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Profile for server {server_name} was not found")
    return profile

@router.delete("/{server_name}", status_code=status.HTTP_204_NO_CONTENT)
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

@router.put("/{server_name}")
# def update_profile(server_name: str, profile: ProfileCreate, db: Session = Depends(get_db)):
def update_profile(server_name: str, profile: schemas.ProfileBase, db: Session = Depends(get_db)):
    profileq = db.query(models.Profile).filter(models.Profile.name == server_name)
    existing_profile = profileq.first()
    if existing_profile == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Profile for server {server_name} does not exists")
    else:
        profileq.update(profile.dict(), synchronize_session=False)
        db.commit()
        # return { "profile" : profileq.first()}
        return profileq.first()
