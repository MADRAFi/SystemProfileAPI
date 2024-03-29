
from typing import Literal


profilespath = "profiles/"
templatespath = "templates/"
isosourcepath = "iso/"
kickstart_file = 'ks.cfg'
isolinux_file = 'isolinux.cfg'
kickstart_template_prefix = "ks_"
isolinux_template_prefix = "isolinux_"
template_sufix = ".jinja2"
isofile_sufix = ".boot.iso"
isosource = {
    'rhel_7' : 'rhel-7.9-x86_64-boot.iso',
    'rhel_8' : 'rhel-8.5-x86_64-boot.iso',
    'rhel_9' : 'rhel-baseos-9.0-beta-0-x86_64-boot.iso'
}


timezone = "America/New_York"
language = "en_us"
keyboard = "us"

timezone_list = Literal[
        'America/New_York',
        'Europe/Warsaw',
        'Asia/Singapore'
    ]

language_list = Literal[
        'en_us',
        'jp_jp',
        'de_de'
    ]
keyboard_list = Literal[
        'us',
        'jp',
        'de'
    ]

json = {}

disk_layout = {
    "boot": 1024,
    "swap": 2048,
    "root": 2048,
    "tmp": 2048,
    "home": 2048,
    "var": 1024,
    "opt": 1024
}

# disk_layout = """
# zerombr
# clearpart --all --initlabel

# part raid.11 --size 1000 --asprimary --ondrive=hda
# part raid.12 --size 1000 --asprimary --ondrive=hda
# part raid.13 --size 2000 --asprimary --ondrive=hda
# part raid.14 --size 8000 --ondrive=hda
# part raid.15 --size 16384 --grow --ondrive=hda
# part raid.21 --size 1000 --asprimary --ondrive=hdc
# part raid.22 --size 1000 --asprimary --ondrive=hdc
# part raid.23 --size 2000 --asprimary --ondrive=hdc
# part raid.24 --size 8000 --ondrive=hdc
# part raid.25 --size 16384 --grow --ondrive=hdc

# # You can add --spares=x
# raid / --fstype xfs --device root --level=RAID1 raid.11 raid.21
# raid /safe --fstype xfs --device safe --level=RAID1 raid.12 raid.22
# raid swap --fstype swap --device swap --level=RAID1 raid.13 raid.23
# raid /usr --fstype xfs --device usr --level=RAID1 raid.14 raid.24
# raid pv.01 --fstype xfs --device pv.01 --level=RAID1 raid.15 raid.25

# # LVM configuration so that we can resize /var and /usr/local later
# volgroup sysvg pv.01
# logvol /var --vgname=sysvg --size=8000 --name=var
# logvol /var/freespace --vgname=sysvg --size=8000 --name=freespacetouse
# logvol /usr/local --vgname=sysvg --size=1 --grow --name=usrlocal
# """

