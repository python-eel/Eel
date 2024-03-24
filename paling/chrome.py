import sys, subprocess as sps, os
from typing import List, Optional

from paling.types import OptionsDictT

# Every browser specific module must define run(), find_path() and name like this

name: str = 'Google Chrome/Chromium'

def run(path: str, options: OptionsDictT, start_urls: List[str]) -> None:
    """
    Run the Chrome browser with the specified path, options, and start URLs.

    Args:
        path (str): The path to the Chrome browser executable.
        options (OptionsDictT): A dictionary containing the options for running Chrome.
        start_urls (List[str]): A list of URLs to open in Chrome.

    Raises:
        TypeError: If the 'cmdline_args' option is not of type List[str].

    Returns:
        None
    """
    if not isinstance(options['cmdline_args'], list):
        raise TypeError("'cmdline_args' option must be of type List[str]")
    if options['app_mode']:
        for url in start_urls:
            sps.Popen([path, '--app=%s' % url] +
                       options['cmdline_args'],
                       stdout=sps.PIPE, stderr=sps.PIPE, stdin=sps.PIPE)
    else:
        args: List[str] = options['cmdline_args'] + start_urls
        sps.Popen([path, '--new-window'] + args,
                   stdout=sps.PIPE, stderr=sys.stderr, stdin=sps.PIPE)


def find_path() -> Optional[str]:
    """
    Finds the path of the Chrome executable based on the current operating system.

    Returns:
        Optional[str]: The path of the Chrome executable if found, otherwise None.
    """
    if sys.platform in ['win32', 'win64']:
        return _find_chrome_win()
    elif sys.platform == 'darwin':
        return _find_chrome_mac() or _find_chromium_mac()
    elif sys.platform.startswith('linux'):
        return _find_chrome_linux()
    else:
        return None


def _find_chrome_mac() -> Optional[str]:
    """
    Find the path of Google Chrome executable on macOS.

    Returns:
        Optional[str]: The path of Google Chrome executable if found, otherwise None.
    """
    default_dir = r'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    if os.path.exists(default_dir):
        return default_dir
    # use mdfind ci to locate Chrome in alternate locations and return the first one
    name = 'Google Chrome.app'
    alternate_dirs = [x for x in sps.check_output(["mdfind", name]).decode().split('\n') if x.endswith(name)]
    if len(alternate_dirs):
        return alternate_dirs[0] + '/Contents/MacOS/Google Chrome'
    return None


def _find_chromium_mac() -> Optional[str]:
    """
    Find the Chromium executable path on macOS.

    Returns:
        Optional[str]: The path to the Chromium executable if found, None otherwise.
    """
    default_dir = r'/Applications/Chromium.app/Contents/MacOS/Chromium'
    if os.path.exists(default_dir):
        return default_dir
    # use mdfind ci to locate Chromium in alternate locations and return the first one
    name = 'Chromium.app'
    alternate_dirs = [x for x in sps.check_output(["mdfind", name]).decode().split('\n') if x.endswith(name)]
    if len(alternate_dirs):
        return alternate_dirs[0] + '/Contents/MacOS/Chromium'
    return None


def _find_chrome_linux() -> Optional[str]:
    """
    Finds the path of the Chrome executable on a Linux system.

    Returns:
        Optional[str]: The path of the Chrome executable if found, None otherwise.
    """
    import whichcraft as wch
    chrome_names = ['chromium-browser',
                    'chromium',
                    'google-chrome',
                    'google-chrome-stable']

    for name in chrome_names:
        chrome = wch.which(name)
        if chrome is not None:
            return chrome # type: ignore # whichcraft doesn't currently have type hints
    return None


def _find_chrome_win() -> Optional[str]:
    """
    Find the path of the Chrome executable on Windows.

    Returns:
        Optional[str]: The path of the Chrome executable if found, None otherwise.
    """
    import winreg as reg
    reg_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe'
    chrome_path: Optional[str] = None

    for install_type in reg.HKEY_CURRENT_USER, reg.HKEY_LOCAL_MACHINE:
        try:
            reg_key = reg.OpenKey(install_type, reg_path, 0, reg.KEY_READ)
            chrome_path = reg.QueryValue(reg_key, None)
            reg_key.Close()
            if not os.path.isfile(chrome_path):
                continue
        except WindowsError:
            chrome_path = None
        else:
            break

    return chrome_path
