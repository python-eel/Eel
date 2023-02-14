import os
import subprocess as sps
import sys
from typing import List

from eel.types import OptionsDictT

name: str = "Edge"


def run(path: str, options: OptionsDictT, start_urls: List[str]) -> None:
    if path != "edge_legacy":
        if options["app_mode"]:
            for url in start_urls:
                sps.Popen([path, "--app=%s" % url] + options["cmdline_args"], stdout=sps.PIPE, stderr=sps.PIPE, stdin=sps.PIPE)
        else:
            args = options["cmdline_args"] + start_urls
            sps.Popen([path, "--new-window"] + args, stdout=sps.PIPE, stderr=sps.PIPE, stdin=sps.PIPE)
    else:
        cmd = "start microsoft-edge:{}".format(start_urls[0])
        sps.Popen(cmd, stdout=sps.PIPE, stderr=sps.PIPE, stdin=sps.PIPE, shell=True)


def find_path() -> bool:
    if sys.platform in ["win32", "win64"]:
        return _find_edge_win()
    else:
        return None


def _find_edge_win():
    import winreg as reg

    reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe"

    for install_type in reg.HKEY_CURRENT_USER, reg.HKEY_LOCAL_MACHINE:
        try:
            reg_key = reg.OpenKey(install_type, reg_path, 0, reg.KEY_READ)
            edge_path = reg.QueryValue(reg_key, None)
            reg_key.Close()
            if not os.path.isfile(edge_path):
                continue
        except WindowsError:
            edge_path = "edge_legacy"
        else:
            break

    return edge_path
