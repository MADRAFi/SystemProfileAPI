# from passlib.context import CryptContext
# import bcrypt, base64
import hashlib

from os import makedirs, getcwd

from . import schemas, constants
from jinja2 import Template


# pwd_context = CryptContext(schemes=["bcrypt"])

# def hash_password(password):
def hash_password(password: str):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    # hashed = bcrypt.hashpw(
    #     base64.b64encode(hashlib.sha256(password.encode()).digest()),
    #     bcrypt.gensalt()
    # )
    # hashed = pwd_context.hash(password)
    return hashed

def save_profile(rootpath: str,  profile: schemas.Profile ):
   
    path = rootpath + profile.fqdn
    try:

        makedirs(path, exist_ok=True)

        definition = {
            'timezone': profile.timezone,
            'language': profile.language,
            'keyboard': profile.keyboard,
            'password': profile.default_pass,
            'fqdn': profile.fqdn
        }
        
        # read ks template
        ksfile = 'ks_rhel9.cfg'

        with open(constants.templatespath + ksfile, 'r') as t:
            template = Template(t.read())
        result = template.render(definition)
        t.close()

        # save
        with open(path + '/' + constants.kickstart_file, 'w') as f:
            f.write(result)
            f.write('ip=' + profile.ip )
        f.close()

    except Exception as error:
        print("Error:", error)
        return str(error)

