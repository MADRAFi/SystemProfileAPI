# from passlib.context import CryptContext
# import bcrypt, base64
import hashlib
from os import makedirs

# from . import schemas, constants
from . import models, schemas, constants
from sqlalchemy.orm.session import Session
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

def save_profile(path: str, os_name: str, profile: schemas.Profile):
   
    # path = rootpath + profile.fqdn
    definition = {
        'timezone': profile.timezone,
        'language': profile.language,
        'keyboard': profile.keyboard,
        'password': profile.default_pass,
        'ip': profile.ip,
        'netmask': profile.netmask,
        'gateway': profile.gateway,
        'fqdn': profile.fqdn
    }
    ks_template = constants.kickstart_template_prefix + os_name + constants.template_sufix
    isolinux_template = constants.isolinux_template_prefix + os_name + constants.template_sufix

    try:
        makedirs(path, exist_ok=True)
        
        # read ks template
        with open(constants.templatespath + ks_template, 'r') as t:
            template = Template(t.read())
            result = template.render(definition)
        t.close()

        # save
        with open(path + '/' + constants.kickstart_file, 'w') as f:
            f.write(result)
        f.close()


        # read isolinux template
        with open(constants.templatespath + isolinux_template, 'r') as t:
            template = Template(t.read())
            result = template.render(definition)
        t.close()

        # save
        with open(path + '/' + constants.isolinux_file, 'w') as f:
            f.write(result)
        f.close()
        
    except Exception as error:
        print("Error:", error)
        return str(error)
