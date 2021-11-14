
from pydantic import BaseModel
from api.models import SystemOS

class SystemBase(BaseModel):
    name: str


class BaselineBase(BaseModel):
    id: int
    name: str
    url: str
    system_id: SystemBase

class BaselineCreate(BaseModel):
    name: str
    url: str
    system_os: str
    class Config:
        orm_mode = True

class BaselineResponse(BaseModel):
    name: str
    # url: str
    # system_id: SystemBase
    class Config:
        orm_mode = True

class ProfileOut(BaseModel):
    fqdn: str
    ip: str
    netmask: str
    gateway: str    
    class Config:
        orm_mode = True

class ProfileCreate(ProfileOut):
    os_name: str
    baseline_name: str
    password: str
    class Config:
        orm_mode = True

class ProfileUpdate(ProfileOut):
    fqdn: str
    baseline_id: int
    ip: str
    netmask: str
    gateway: str
    default_pass: str