import platform
import subprocess as sps
import sys

name = "Edge"


def run(_path, options, start_urls):
    cmd = "start microsoft-edge:{}".format(start_urls[0])
    sps.Popen(cmd, stdout=sps.PIPE, stderr=sps.PIPE, stdin=sps.PIPE, shell=True)


def find_path():
    if platform.system() == "Windows":
        return True

    return False
