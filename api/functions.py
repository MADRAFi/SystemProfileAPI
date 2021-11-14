from passlib.context import CryptContext
from os import makedirs
from api import schemas

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated_method="auto")
pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str):
    return pwd_context.hash(password)


def save_profile(path: str,  profile: schemas.ProfileCreate ):
   
    kickstart_file = 'ks.cfg'

    try:
        makedirs(path + profile.fqdn, exist_ok=True)
        f = open(path + kickstart_file, 'w')
        f.write('ip=' + profile.ip )

    except Exception as error:
        print("Error:", error.__cause__)
        return str(error.__cause__)
    
