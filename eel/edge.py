import platform
import subprocess as sps
import sys
from typing import List

from eel.types import OptionsDictT

name: str = 'Edge'


def run(_path: str, options: OptionsDictT, start_urls: List[str]) -> None:
    cmd = 'start microsoft-edge:{}'.format(start_urls[0])
    sps.Popen(cmd, stdout=sps.PIPE, stderr=sps.PIPE, stdin=sps.PIPE, shell=True)

def find_path() -> bool:
    if platform.system() == 'Windows':
        return True

    return False
