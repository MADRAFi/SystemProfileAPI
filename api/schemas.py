
from typing import Optional
from pydantic import BaseModel
from . import constants
# from api.models import SystemOS

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

# class localization(BaseModel):
#     timezone: Literal[
#             'America/New_York',
#             'Europe/Warsaw',
#             'Asia/Singapore'
#         ]

class JsonData(BaseModel):
    # runlist: Optional[str]
    # auth_model: Optional[str]
    runlist: str
    auth_model: str

class DiskLayout(BaseModel):
    boot: int
    swap: int
    root: int
    tmp: int
    home: int
    var: int
    opt: int
    

class Profile(BaseModel):
    fqdn: str
    baseline_id: int
    ip: str
    netmask: str
    gateway: str
    default_pass: str
    mac_address: Optional[str]
    # disk_layout: Optional[BLOB]
    disk_layout: Optional[DiskLayout] = None
    jsondata: Optional[JsonData] = None
    timezone: constants.timezone_list
    language: constants.language_list
    keyboard: constants.keyboard_list
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

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
    mac_address: Optional[str]
    # disk_layout: Optional[BLOB]
    disk_layout: Optional[DiskLayout] = None
    jsondata: Optional[JsonData] = None
    timezone: constants.timezone_list
    language: constants.language_list
    keyboard: constants.keyboard_list
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class ProfileUpdate(ProfileOut):
    fqdn: str
    os_name: str
    baseline_name: str
    ip: str
    netmask: str
    gateway: str
    password: str
    mac_address: Optional[str] = None
    # disk_layout: Optional[BLOB]
    disk_layout: Optional[DiskLayout] = None
    jsondata: Optional[JsonData] = None
    timezone: constants.timezone_list
    language: constants.language_list
    keyboard: constants.keyboard_list
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
