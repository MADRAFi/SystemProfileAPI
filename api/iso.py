try:
    from io import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from os import makedirs
import pycdlib

from api import constants


def create(path: str, os_name: str, iso_file: str):
    try:
        iso = pycdlib.PyCdlib()

        # print(constants.isosource[os_name])
        iso_source = constants.isosource[os_name]
        iso.open(constants.isosourcepath + iso_source)
        

        iso.rm_file(joliet_path='/images/install.img')
        iso.rm_file(joliet_path='/isolinux/isolinux.cfg')
        iso.add_file(path + '/' + constants.isolinux_file, joliet_path='/isolinux/' + constants.isolinux_file)
        
        makedirs(path, exist_ok=True)
        iso.write(path + '/' + iso_file)
        iso.close()

    except Exception as error:
        print("Error:", error)
        return str(error)