
from typing import Literal


profilespath = 'profiles/'
templatespath = 'templates/'
kickstart_file = 'ks.cfg'
timezone = "America/New_York"
language = "en_US.UTF-8"
keyboard = "us"

timezone_list = Literal[
        'America/New_York',
        'Europe/Warsaw',
        'Asia/Singapore'
    ]

language_list = Literal[
        'en_US.UTF-8',
        'jp_jp',
        'de_de'
    ]
keyboard_list = Literal[
        'us',
        'jp',
        'de'
    ]

disk_layout = """
zerombr
clearpart --all --initlabel

part raid.11 --size 1000 --asprimary --ondrive=hda
part raid.12 --size 1000 --asprimary --ondrive=hda
part raid.13 --size 2000 --asprimary --ondrive=hda
part raid.14 --size 8000 --ondrive=hda
part raid.15 --size 16384 --grow --ondrive=hda
part raid.21 --size 1000 --asprimary --ondrive=hdc
part raid.22 --size 1000 --asprimary --ondrive=hdc
part raid.23 --size 2000 --asprimary --ondrive=hdc
part raid.24 --size 8000 --ondrive=hdc
part raid.25 --size 16384 --grow --ondrive=hdc

# You can add --spares=x
raid / --fstype xfs --device root --level=RAID1 raid.11 raid.21
raid /safe --fstype xfs --device safe --level=RAID1 raid.12 raid.22
raid swap --fstype swap --device swap --level=RAID1 raid.13 raid.23
raid /usr --fstype xfs --device usr --level=RAID1 raid.14 raid.24
raid pv.01 --fstype xfs --device pv.01 --level=RAID1 raid.15 raid.25

# LVM configuration so that we can resize /var and /usr/local later
volgroup sysvg pv.01
logvol /var --vgname=sysvg --size=8000 --name=var
logvol /var/freespace --vgname=sysvg --size=8000 --name=freespacetouse
logvol /usr/local --vgname=sysvg --size=1 --grow --name=usrlocal
"""

