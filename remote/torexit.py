#!/usr/bin/env python3
#
# A simple module to search the IP address against known TOR exit nodes.
# This module will use a [cached database](https://check.torproject.org/exit-addresses)
# and sets the cache TTL for 24 hours.  (no point in hammering TOR)
#

import urllib.request
import sys
import os
from datetime import datetime
from datetime import timedelta

debug = False

# run this only every 24 hours, or on first run.
def fetch_exit_db(exit_filename="tor-exit-addresses"):
	cache_url = "https://check.torproject.org/exit-addresses"
	exitdb_fh = ""
	exitdb = []

	# Open the database file for overwriting.
	try:
		exitdb_fh = open(exit_filename, 'w')
	except:
		if debug:
			print("Unable to open() database file for writing: %s", exit_filename)
		return "file_error"

	# Fetch the database
	try:
		response = urllib.request.urlopen(cache_url).read()
	except:
		if debug:
			print("Unable to fetch remote database.")
		return "request_error"
	# Parse out the bits we need, just the IP address.
	for line in response.decode('utf-8').split("\n"):
		if line.startswith("ExitAddress"):
			exitdb.append(line.split(" ")[1])

	# Write out the database, one IP per line, for easy reading.
	exitdb_fh.write("\n".join(exitdb))
	exitdb_fh.close()
	return True

# Makes a
def load_exit_db(exit_filename="tor-exit-addresses"):
	try:
		os.stat(exit_filename)
	except:
		if debug:
			print("Unable stat() database file: %s" % exit_filename)
		return "load_error"

	try:
		raw = open(exit_filename).read().strip()
	except:
		if debug:
			print("Unable to open() database file: %s" % exit_filename)
		return "read_error"

	return raw.split("\n")


# is the database more than 24 hours old?  If so, fetch
# a new one.
def check_exit_db(exit_filename="tor-exit-addresses"):
	exit_time = datetime.fromtimestamp(os.stat(exit_filename).st_mtime)
	now = datetime.now()
	exit_age = now - exit_time
	if exit_age.seconds > 86400:
		retval = fetch_exit_db(exit_filename)
		if retval != True:
			if debug:
				print("Database update failure.")
			return "update_error"
		else:
			if debug:
				print("Database update successful.")
			return "update_success"
	else:
		if debug:
			print("Database less than a day old, not updating.")
		return "update_cached"

def search_tor_exitdb(target_ip):
	retval = check_exit_db("./remote/tor-exit-addresses")
	if retval == "update_error":
		return "request_error"
	db = load_exit_db("./remote/tor-exit-addresses")
	if target_ip in db:
		if debug:
			print("Match found.  IP: %s in database." % target_ip)
		return True
	return False


if __name__ == "__main__":
    print(search_tor_exitdb(sys.argv[1]))
