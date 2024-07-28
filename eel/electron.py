#from __future__ import annotations
import sys
import os
import subprocess as sps
import whichcraft as wch
from typing import List, Optional

from eel.types import OptionsDictT

name: str = 'Electron'

def run(path: str, options: OptionsDictT, start_urls: List[str]) -> None:
    if not isinstance(options['cmdline_args'], list):
        raise TypeError("'cmdline_args' option must be of type List[str]")
    cmd = [path] + options['cmdline_args']
    cmd += ['.', ';'.join(start_urls)]
    sps.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr, stdin=sps.PIPE)


def find_path() -> Optional[str]:
    if sys.platform in ['win32', 'win64']:
        return r'..\node_modules\electron\dist\electron.exe'
    elif sys.platform in ['darwin', 'linux']:
        # This should work find...
        return wch.which('electron') # type: ignore # whichcraft doesn't currently have type hints
    else:
        return None

