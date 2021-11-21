from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey
from .database import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import JSON, TIMESTAMP, Integer
from . import constants


class Profile(Base):
    __tablename__ = "profiles"
 
    fqdn = Column(String, primary_key=True, nullable=False, unique=True, index=True)
    # fqdn = Column(String, nullable=False)
    baseline_id = Column(Integer, ForeignKey('baselines.id'), nullable=False, index=True)
    ip = Column(String, nullable=False)
    netmask = Column(String, nullable=False)
    gateway = Column(String, nullable=False)
    mac_address = Column(String, nullable=True)
    default_pass = Column(String, nullable=False)
    # disk_layout = Column(BLOB, nullable=False, default=constants.disk_layout)
    disk_layout = Column(JSON, nullable=False, default=constants.disk_layout)
    jsondata = Column(JSON, nullable=False, default=constants.json); alias='json'
    timezone = Column(String, nullable=False, default=constants.timezone)
    language = Column(String, nullable=False, default=constants.language)
    keyboard = Column(String, nullable=False, default=constants.keyboard)
    created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("(datetime())"))

    baselines = relationship("Baseline", back_populates="profiles")

class Baseline(Base):
    __tablename__ = "baselines"
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    name = Column(String, nullable=False, index=True)
    system_id = Column(Integer, ForeignKey('systems.id'), nullable=False, index=True)
    url = Column(String, nullable=False)

    systemos = relationship("SystemOS", back_populates="baselines")
    profiles = relationship("Profile", back_populates="baselines")

class SystemOS(Base):
    __tablename__ = "systems"
 
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    name = Column(String, nullable=False, unique=True)

    baselines = relationship("Baseline", back_populates="systemos")