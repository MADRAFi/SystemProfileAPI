# from passlib.context import CryptContext
import bcrypt, base64, hashlib
from os import makedirs, getcwd
from . import schemas, constants
from string import Template

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

def save_profile(rootpath: str,  profile: schemas.ProfileCreate ):
   
    path = rootpath + profile.fqdn
    try:

        makedirs(path, exist_ok=True)

        definition = {
            'title': 'This is the title',
            'subtitle': 'And this is the subtitle',
            'password': 'pass',
            'GRUB': "'/^GRUB_CMDLINE_LINUX=/{s/(\s*)(rhgb|quiet)\s*/\1/g;};' -e '/^GRUB_CMDLINE_LINUX=/{s/(\s*)$/ console=ttyS0 console=tty1\"/;}' /etc/default/grub"
        }
        
        # read template
        ksfile = 'rhel9.cfg'
        with open(constants.templatespath + ksfile, 'r') as t:
            template = Template(t.read())
            result = template.substitute(definition)
        t.close()
        
        # save
        with open(path + '/' + constants.kickstart_file, 'w') as f:
            f.write(result)
            f.write('ip=' + profile.ip )
        f.close()

    except Exception as error:
        print("Error:", error)
        return str(error)

