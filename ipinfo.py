#!/usr/bin/env python3
#
# ipinfo.py
#
# Tells you everything it can about a given IP address, based on whatever
# modules and internet infrastructure are available.
#

import sys, json, argparse, collections

# FIXME: clean up the module structure here.
from local import dnstests
from local import whois
from local import geoiplookup
from remote import virustotal
from remote import torexit

# Parse options.  You want to divide them into three groups: those that are
# externally rate limited with --slow (e.g. VirusTotal, 4 requests/min), those
# who are external, but *not* rate limited (i.e.: --external), and those that
# are reliant on general infrastructure available to all (--local).  The default
# should be --local IMO, but for some reason, you may want to not specify those.
parser = argparse.ArgumentParser()
parser.add_argument('-l', '--local', dest='local', action='store_true',
                    help='Enable checks based on local internet infrastructure.')
parser.add_argument('-e', '--external', dest='external', action='store_true',
                    help='Enable checks based on remote, internet accessible systems.')
parser.add_argument('-s', '--slow', dest='slow', action='store_true',
                    help='Enable checks via internet services with a known rate-limit')
parser.add_argument('ip', nargs=1, metavar="IP",
                    help="IP Address to examine.")
# CSV and JSON output are mutually exclusive.
group = parser.add_mutually_exclusive_group()
group.add_argument('-j','--json', dest='json', action='store_true',
                    help='Output in JSON format.')
group.add_argument('-t', '--tsv', dest='tsv', action='store_true',
                    help='Output in TSV format.')
try:
    args = parser.parse_args()
except argparse.ArgumentError:
    # FIXME: This doesn't work. I can't seem to catch the right exception type here.
    print("Conflicting options given.")
    sys.exit(2)
except:
    print("Unable to parse arguments on the command line.")
    sys.exit(2)

# If no type arguments are pased, assume --local
if not (args.local or args.slow or args.external):
    args.local = True

# If no format arguments are pased, assume JSON
if not (args.json or args.tsv):
    args.json = True

# IP is required, obviously. Do nothing wtihtout it.
if args.ip == None:
    print("No IP address given.")
    sys.exit(2)
else:
    # FIXME: Validate IPv4 input address here.
    target_ip = args.ip[0]

json_data = [target_ip,collections.OrderedDict()]

json_data[1]['PTR'] = dnstests.resolve_ip(target_ip)
json_data[1]['Contact'] = whois.whois_ip(target_ip)
json_data[1]['Country'] = geoiplookup.get_location(target_ip)
tor_exits = torexit.search_tor_exitdb(target_ip)
if tor_exits != "request_error":
	json_data[1]['Tor Exit'] = tor_exits

if args.slow:
    vt = virustotal.search_vtotal_api(target_ip)
    if vt not in [ 'request_error', 'parse_error']:
        json_data[1]['VT:Resolutions'] = vt['num_resolutions']
        json_data[1]['VT:URLs'] = vt['num_urls']

if args.json:
    print(json.dumps(json_data))
elif args.tsv:
    print("\t".join(json_data[1].keys()))
    print("\t".join(json_data[1].values()))

sys.exit(0)
