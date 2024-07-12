import subprocess as sps
import sys
from typing import List, Optional

from eel.types import OptionsDictT

name: str = 'Edge'


def run(path: str, options: OptionsDictT, start_urls: List[str]) -> None:
    if path.startswith('start microsoft-edge:'):
        cmd = 'start microsoft-edge:{}'.format(start_urls[0])
        sps.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr, stdin=sps.PIPE, shell=True)
    else:
        args: List[str] = options['cmdline_args'] + start_urls  # type: ignore
        sps.Popen([path, '--new-window'] + args,
                  stdout=sps.PIPE, stderr=sys.stderr, stdin=sps.PIPE)


def find_path() -> Optional[str]:
    if sys.platform in ['win32', 'win64']:
        return _find_edge_win()
    elif sys.platform.startswith('linux'):
        return _find_edge_linux()
    else:
        return None


def _find_edge_linux() -> Optional[str]:
    import whichcraft as wch
    return wch.which('microsoft-edge') # type: ignore # whichcraft doesn't currently have type hints


def _find_edge_win() -> str:
    return 'start microsoft-edge:'
