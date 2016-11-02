#!/usr/bin/env python3
#
# A simple module to search the IP address against VirusTotal's API
# WARNING: Rate limited to one API call every 15 seconds (or, 4 per minute).
#          Probably hardcode a sleep() call for 16 seconds just to be under
#          the limit when this module is enabled.
# [Howto](https://www.virustotal.com/en/documentation/public-api/#getting-ip-reports)
#

import urllib.request
import json, sys
from time import sleep

def _load_key():
    vtapikey = open('./remote/virustotalapikey').read().strip()
    #FIXME Validate that it's a hex string that's 140 characters long
    return vtapikey

def search_vtotal_api(target_ip):
    uri = 'https://www.virustotal.com/vtapi/v2/ip-address/report'
    parameters = {'ip':target_ip, 'apikey':_load_key()}
    try:
        response = urllib.request.urlopen('%s?%s' %(uri,urllib.parse.urlencode(parameters))).read()
        sleep(15)   # this is because there's a limit of 4 requests per minute to Virustotal's API
    except:
        return "request_error"
    try:
        # this is a python3ism with strings vs binaries, etc.
        # See: https://stackoverflow.com/questions/6862770/python-3-let-json-object-accept-bytes-or-let-urlopen-output-strings
        data = json.loads(response.decode('utf8'))
    except:
        return "parse_error"
    if data['response_code'] != 1:
        return {'num_resolutions': 0, 'num_urls': 0}
    else:
        #FIXME add a "dump all data" debug type flag to this module for use here
        return {'num_resolutions': len(data['resolutions']), 'num_urls': len(data['detected_urls'])}

if __name__ == "__main__":
    print(search_vtotal_api(sys.argv[1]))
