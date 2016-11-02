#!/usr/bin/env python3
#
# Wraps the whois binary.  I'm really surprised there's no simple
# pure-python whois library, and that I have to use subprocess
# to do this, given that all whois is is telnet to port 43.

import sys
import subprocess

def whois_ip(target_ip):
    orgname = ''
    orgemail = ''
    ph = subprocess.Popen(['whois',str(target_ip)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    so = ph.communicate()[0]
    for line in so.decode().splitlines():
        #FIXME: there's a whole lot of *NICs out there where this won't work.
        #       See `whois 14.1.2.3` for example of APNIC.
        if line.startswith('OrgName'):
            orgname = line.split(':')[1].lstrip()
        if line.startswith('OrgAbuseEmail'):
            orgemail = line.split(':')[1].lstrip()
    return "%s <%s>" % (orgname,orgemail)
    
if __name__ == "__main__":
    print(whois_ip(sys.argv[1]))

