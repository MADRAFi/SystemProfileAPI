
from pydantic import BaseModel

from api.models import SystemOS

class ProfileBase(BaseModel):
    name: str
    fqdn: str
    ip: str
    netmask: str
    gateway: str

# class ProfileCreate(ProfileBase):
#     pass

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