import sys
import os
import subprocess as sps
import whichcraft as wch

name = 'Electron'

def run(path, options, start_urls):
    cmd = [path] + options['cmdline_args']
    cmd += ['.', ';'.join(start_urls)]
    sps.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr, stdin=sps.PIPE)


def find_path():
    if sys.platform in ['win32', 'win64']:
        return r'..\node_modules\electron\dist\electron.exe'
    elif sys.platform in ['darwin', 'linux']:
        # This should work find...
        return wch.which('electron')
    else:
        return None

