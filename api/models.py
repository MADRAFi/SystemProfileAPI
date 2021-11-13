from sqlalchemy.sql.expression import text
from .database import Base
from sqlalchemy import Column, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Profile(Base):
    __tablename__ = "profiles"
 
    # name = Column("name", String, primary_key=True, nullable=False, unique=True)
    # fqdn = Column("fqdn", String, nullable=False)
    # ip = Column("ip", String, nullable=False)
    # netmask = Column("netmask", String, nullable=False)
    # gateway = Column("gateway", String, nullable=False)
    # created = Column("created", TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    name = Column(String, primary_key=True, nullable=False, unique=True)
    fqdn = Column(String, nullable=False)
    ip = Column(String, nullable=False)
    netmask = Column(String, nullable=False)
    gateway = Column(String, nullable=False)
    created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('datetime()'))