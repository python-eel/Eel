import sys, subprocess as sps, os
from typing import Optional

name = 'Edge'

def run(path: str, options: dict, start_urls: list) -> None:
    """
    Run the specified web browser with the given options and start URLs.

    Args:
        path (str): The path to the web browser executable.
        options (dict): A dictionary of options for the web browser.
        start_urls (list): A list of URLs to open in the web browser.

    Returns:
        None
    """
    if path != 'edge_legacy':
        if options['app_mode']:
            for url in start_urls:
                sps.Popen([path, '--app=%s' % url] + options['cmdline_args'], 
                        stdout=sps.PIPE, stderr=sps.PIPE, stdin=sps.PIPE)
        else:
            args = options['cmdline_args'] + start_urls
            sps.Popen([path, '--new-window'] + args,
                    stdout=sps.PIPE, stderr=sys.stderr, stdin=sps.PIPE)
    else:
        cmd = 'start microsoft-edge:{}'.format(start_urls[0])
        sps.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr, stdin=sps.PIPE, shell=True)

def find_path() -> Optional[str]:
    if sys.platform in ['win32', 'win64']:
        return _find_edge_win()
    else:
        return None

def _find_edge_win() -> str:
    """
    Finds the path of the Microsoft Edge browser executable on Windows.

    Returns:
        str: The path of the Microsoft Edge browser executable.
    """
    import winreg as reg
    reg_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe'

    for install_type in reg.HKEY_CURRENT_USER, reg.HKEY_LOCAL_MACHINE:
        try:
            reg_key = reg.OpenKey(install_type, reg_path, 0, reg.KEY_READ)
            edge_path = reg.QueryValue(reg_key, None)
            reg_key.Close()
            if not os.path.isfile(edge_path):
                continue
        except FileNotFoundError:
            edge_path = 'edge_legacy'
        else:
            break

    return edge_path