#!/usr/bin/env python3
#
# Use the local MaxMind database to get a rough
# approximation of the IP country of origin.
# (This originally used a pure python GeoIP module, but
# we're using the Linux C binary `geoiplookup`)
#

import os, subprocess
from stat import *

def get_location(target_ip):
    geoipcmd = os.stat('/usr/bin/geoiplookup')
    if not S_ISREG(geoipcmd.st_mode):
        print("Can't find geoiplookup. `sudo dnf install GeoIP`")
        sys.exit(1)

    ph = subprocess.Popen(['geoiplookup',str(target_ip)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    so = ph.communicate()[0]
    location = so.decode().splitlines()[0].split(':')[1].lstrip()
    return location

if __name__ == "__main__":
    print(get_location(sys.argv[1]))
