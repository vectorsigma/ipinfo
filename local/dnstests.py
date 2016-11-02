#!/usr/bin/env python3
#
# Get some data on an IP address that can be gleaned via DNS
#

import sys

try:
    import dns.resolver
    import dns.reversename
except Exception as e:
    print("Unable to import DNS module. sudo dnf install python3-dns")
    print(e.message)
    sys.exit(1)

def resolve_ip(target_ip):
    try:
        answer = dns.resolver.query(dns.reversename.from_address(target_ip), "PTR")
    except:
        answer = ["None"]
    return str(answer[0])
    

if __name__ == "__main__":
    # Simple test to know the module works.
    print(resolve_ip(sys.argv[1]))
    


