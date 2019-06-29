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
        # It doesn't work well passing the .bat file to Popen, so we get the actual .exe
        bat_path = wch.which('electron')
        return os.path.join(bat_path, r'..\node_modules\electron\dist\electron.exe')
    elif sys.platform in ['darwin', 'linux']:
        # This should work find...
        return wch.which('electron')
    else:
        return None

