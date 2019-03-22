import subprocess as sps

def run(options, start_urls):
	# TODO: Find Eletron properly, e.g. on Windows

	electron_path = '/usr/local/bin/electron'
	sps.Popen([electron_path, '.'] + start_urls,
              stdout=sps.PIPE, stderr=sps.PIPE, stdin=sps.PIPE)

