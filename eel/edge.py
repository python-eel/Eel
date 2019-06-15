import subprocess as sps
import sys

name = 'Edge'


def run(_path, options, start_urls):
    cmd = 'start microsoft-edge:{}'.format(start_urls[0])
    sps.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr, stdin=sps.PIPE, shell=True)


def find_path():
    # Path isn't necessary. Edge is launched with a CLI argument
    return True
