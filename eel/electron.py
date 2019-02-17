import subprocess as sps
import sys

def run(options, start_urls):
	# TODO: Find Eletron properly, e.g. on Windows
	# TODO: check for package.json and print error

	electron_path = '/usr/local/bin/electron'
	sps.Popen([electron_path, '.'] + start_urls,
              stdout=sys.stdout, stderr=sps.PIPE, stdin=sps.PIPE)

