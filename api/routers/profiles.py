from datetime import timezone
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.sql.sqltypes import BLOB
from .. import functions, models, schemas, constants
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

@router.get("/", response_model= List[schemas.ProfileOut])
def get_profiles(db: Session = Depends(get_db)):

    profiles = db.query(models.Profile).all()
    return profiles

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.ProfileOut)
# def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):

    os_name = profile.os_name
    os_id = db.query(models.SystemOS).filter(models.SystemOS.name == os_name).first().id

    baseline_name = profile.baseline_name
    found_baseline_id = db.query(models.Baseline).filter((models.Baseline.system_id == os_id) & (models.Baseline.name == baseline_name)).first().id
    
    new_profile = models.Profile(
        fqdn = profile.fqdn,
        baseline_id = found_baseline_id,
        ip = profile.ip,
        netmask = profile.netmask,
        gateway = profile.gateway,
        default_pass = functions.hash_password(profile.password),
        mac_address = profile.mac_address,
        timezone = profile.timezone,
        language = profile.language,
        keyboard = profile.keyboard

        # disk_layout = profile.disk_layout.encode(BLOB)

    )
    # new_profile = models.Profile(**profile.dict())

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

@router.get("/{server_name}", response_model= schemas.ProfileOut)
def get_profile(server_name: str, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.fqdn == server_name).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Profile for server {server_name} was not found")
    return profile

@router.get("/{server_name}/download", response_model= schemas.ProfileOut)
def get_profile(server_name: str, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.fqdn == server_name).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Profile for server {server_name} was not found")
    else:
        functions.save_profile(constants.profilespath, profile)


    return profile

@router.get("/{server_name}/debug")
def get_profile(server_name: str, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.fqdn == server_name).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Profile for server {server_name} was not found")
    
    return profile

@router.delete("/{server_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(server_name: str, db: Session = Depends(get_db)):
    profileq = db.query(models.Profile).filter(models.Profile.fqdn == server_name)
    profile = profileq.first()
    if profile == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Profile for server {server_name} does not exists")
    else:
        profileq.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{server_name}", response_model= schemas.ProfileOut)
# def update_profile(server_name: str, profile: ProfileCreate, db: Session = Depends(get_db)):
def update_profile(server_name: str, profile: schemas.ProfileUpdate, db: Session = Depends(get_db)):
    profileq = db.query(models.Profile).filter(models.Profile.fqdn == server_name)
    existing_profile = profileq.first()
    if existing_profile == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Profile for server {server_name} does not exists")
    else:
        os_name = profile.os_name
        os_id = db.query(models.SystemOS).filter(models.SystemOS.name == os_name).first().id
        
        baseline_name = profile.baseline_name
        found_baseline_id = db.query(models.Baseline).filter((models.Baseline.system_id == os_id) & (models.Baseline.name == baseline_name)).first().id
        
        new_profile = schemas.Profile(
            fqdn = profile.fqdn,
            baseline_id = found_baseline_id,
            ip = profile.ip,
            netmask = profile.netmask,
            gateway = profile.gateway,
            default_pass = functions.hash_password(profile.password),
            mac_address = profile.mac_address,
            timezone = profile.timezone,
            language = profile.language,
            keyboard = profile.keyboard

            # disk_layout = bytearray(profile.disk_layout)
        )
        profileq.update(new_profile.dict(), synchronize_session=False)
        db.commit()
        # return { "profile" : profileq.first()}
        return new_profile
