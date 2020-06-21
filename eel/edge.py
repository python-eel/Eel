import platform
import subprocess as sps
import sys

name = 'Edge'


def run(_path, options, start_urls):
    proclist = []
    cmd = 'start microsoft-edge:{}'.format(start_urls[0])
    procitem = sps.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr, stdin=sps.PIPE, shell=True)
    proclist.append(procitem)
    return proclist


def find_path():
    if platform.system() == 'Windows':
        return True

    return False
