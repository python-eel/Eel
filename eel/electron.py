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
        if bat_path is not None:
            exe_path = os.path.join(bat_path, r'..\node_modules\electron\dist\electron.exe')
            if os.path.exists(exe_path):
                return exe_path
            else:
                return bat_path
        return None
    elif sys.platform in ['darwin', 'linux']:
        # This should work find...
        return wch.which('electron')
    else:
        return None

