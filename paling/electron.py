#from __future__ import annotations
import sys
import os
import subprocess as sps
import whichcraft as wch
from typing import List, Optional

from paling.types import OptionsDictT

name: str = 'Electron'

def run(path: str, options: OptionsDictT, start_urls: List[str]) -> None:
    """
    Run the specified Electron application.

    Args:
        path (str): The path to the Electron application executable.
        options (OptionsDictT): A dictionary containing options for the Electron application.
        start_urls (List[str]): A list of URLs to open in the Electron application.

    Raises:
        TypeError: If the 'cmdline_args' option is not of type List[str].
    """
    if not isinstance(options['cmdline_args'], list):
        raise TypeError("'cmdline_args' option must be of type List[str]")
    cmd = [path] + options['cmdline_args']
    cmd += ['.', ';'.join(start_urls)]
    sps.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr, stdin=sps.PIPE)


def find_path() -> Optional[str]:
    """
    Finds the path to the Electron executable.

    Returns:
        Optional[str]: The path to the Electron executable if found, otherwise None.
    """
    if sys.platform in ['win32', 'win64']:
        # It doesn't work well passing the .bat file to Popen, so we get the actual .exe
        bat_path = wch.which('electron')
        return os.path.join(bat_path, r'..\node_modules\electron\dist\electron.exe')
    elif sys.platform in ['darwin', 'linux']:
        # This should work fine...
        return wch.which('electron') # type: ignore # whichcraft doesn't currently have type hints
    else:
        return None

