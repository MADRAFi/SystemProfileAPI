from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from api import models, schemas
from api.database import engine, get_db
from sqlalchemy import engine
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import mode


router = APIRouter(
    prefix = "/baselines",
    tags=['Baselines']
)

#######################################################################################################################
# Baselines
#######################################################################################################################

@router.get("/")
def get_baselines(db: Session = Depends(get_db)):

    baselines = db.query(models.Baseline).all()
    return baselines

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_baseline(baseline: schemas.BaselineCreate, db: Session = Depends(get_db)):
    os_name = baseline.system_os
    os_id = db.query(models.SystemOS).filter(models.SystemOS.name == os_name).first().id
    
    new_baseline = models.Baseline(name = baseline.name, url = baseline.url, system_id = os_id)
    # new_baseline = models.Baseline(**baseline.dict())
    
    try:
        db.add(new_baseline)
        db.commit()
        db.refresh(new_baseline)
        return new_baseline
    except Exception as error:
        print("Error:", error.__cause__)
        return str(error.__cause__)

# @api.get("/baselines/{os_name}", response_model=List[schemas.BaselineResponse])
@router.get("/{os_name}")
def get_baselines(os_name: str, db: Session = Depends(get_db)):
# @api.get("/baselines/{os_name}", response_model=schemas.BaselineBase)
# def get_baseline(os_name: str, baselines: schemas.BaselineBase, db: Session = Depends(get_db)):

    os_id = db.query(models.SystemOS).filter(models.SystemOS.name == os_name).first().id
    baselines = db.query(models.Baseline).filter(models.Baseline.system_id == os_id).all()
    # baselines = db.query(models.Baseline).filter(models.SystemOS.name == os_name).all()
    if not baselines:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Baseline for OS {os_name} was not found")
    return baselines

@router.delete("/{os_name}/{baseline_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_baseline(os_name: str, baseline_name: str, db: Session = Depends(get_db)):
    os_id = db.query(models.SystemOS).filter(models.SystemOS.name == os_name).first().id
    baselineq = db.query(models.Baseline).filter((models.Baseline.system_id == os_id) & (models.Baseline.name == baseline_name))
    #  and (models.Baseline.name == baseline_name))
    baseline = baselineq.first()
    if baseline == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Baseline for OS {baseline_name} does not exists")
    else:
        baselineq.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)