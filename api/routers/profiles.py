from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from starlette.responses import FileResponse
from .. import functions, models, schemas, constants, iso
from api.database import get_db
from sqlalchemy.orm.session import Session

router = APIRouter(
    prefix= "/profiles",
    tags=['Profiles']
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
    osq = db.query(models.SystemOS).filter(models.SystemOS.name == os_name).first()

    if osq == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"OS {os_name} does not exist")

    baseline_name = profile.baseline_name
    baselineq = db.query(models.Baseline).filter((models.Baseline.system_id == osq.id) & (models.Baseline.name == baseline_name)).first()
    if baselineq == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Baseline {baseline_name} for {os_name} does not exist")

    new_profile = models.Profile(
        fqdn = profile.fqdn,
        baseline_id = baselineq.id,
        ip = profile.ip,
        netmask = profile.netmask,
        gateway = profile.gateway,
        default_pass = functions.hash_password(profile.password),
        mac_address = profile.mac_address or '',
        disk_layout = profile.disk_layout or constants.disk_layout,
        jsondata = profile.jsondata or constants.json,
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
        # profileq = db.query(models.Baseline, models.SystemOS).filter(models.Baseline.id == profile.baseline_id).filter(models.SystemOS.id == models.Baseline.system_id).first()
        # os_name = profileq.name

        system_id = db.query(models.Baseline).filter(models.Baseline.id == profile.baseline_id).first().system_id
        os_name = db.query(models.SystemOS).filter(models.SystemOS.id == system_id).first().name.lower()

        rootpath = constants.profilespath + profile.fqdn
        isofile = profile.fqdn + constants.isofile_sufix
        functions.save_profile(rootpath, os_name, profile)
        iso.create(rootpath, os_name, isofile)


    return FileResponse(rootpath + '/' + isofile, media_type='application/octet-stream', filename=isofile)

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
                            detail=f"Profile for server {server_name} does not exist")
    if profile.fqdn != server_name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Provided server {server_name} is different then specified in json {profile.fqdn}")
    else:
        os_name = profile.os_name
        osq = db.query(models.SystemOS).filter(models.SystemOS.name == os_name).first()
        if osq == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"OS {os_name} does not exist")
        
        baseline_name = profile.baseline_name
        baselineq = db.query(models.Baseline).filter((models.Baseline.system_id == osq.id) & (models.Baseline.name == baseline_name)).first()
        if baselineq == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Baseline {baseline_name} for OS {os_name} does not exist")
        
        
        # print(profile.jsondata)
        new_profile = schemas.Profile(
            fqdn = profile.fqdn,
            baseline_id = baselineq.id,
            ip = profile.ip,
            netmask = profile.netmask,
            gateway = profile.gateway,
            default_pass = functions.hash_password(profile.password),
            mac_address = profile.mac_address or '',
            disk_layout = profile.disk_layout or constants.disk_layout,
            jsondata = profile.jsondata or constants.json,
            timezone = profile.timezone,
            language = profile.language,
            keyboard = profile.keyboard
        )
        # new_profile = models.Profile(
        #     baseline_id = found_baseline_id,
        #     default_pass = functions.hash_password(profile.password),
        #     **dict_profile
        # )
        
        profileq.update(new_profile.dict(), synchronize_session=False)
        db.commit()
        return new_profile
