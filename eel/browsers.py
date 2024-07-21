import subprocess as sps
import webbrowser as wbr
from typing import Union, List, Dict, Iterable, Optional
from types import ModuleType

from eel.types import OptionsDictT
import eel.chrome as chm
import eel.electron as ele
import eel.edge as edge
#import eel.firefox as ffx      TODO
#import eel.safari as saf       TODO

_browser_paths: Dict[str, str] = {}
_browser_modules: Dict[str, ModuleType] = {'chrome':   chm,
                                           'electron': ele,
                                           'edge': edge}


def _build_url_from_dict(page: Dict[str, str], options: OptionsDictT) -> str:
    scheme = page.get('scheme', 'http')
    host = page.get('host', 'localhost')
    port = page.get('port', options["port"])
    path = page.get('path', '')
    if not isinstance(port, (int, str)):
        raise TypeError("'port' option must be an integer")
    return '%s://%s:%d/%s' % (scheme, host, int(port), path)


def _build_url_from_string(page: str, options: OptionsDictT) -> str:
    if not isinstance(options['port'], (int, str)):
        raise TypeError("'port' option must be an integer")
    base_url = 'http://%s:%d/' % (options['host'], int(options['port']))
    if "http" in page:
        return page
    else:
        return base_url + page


def _build_urls(start_pages: Iterable[Union[str, Dict[str, str]]], options: OptionsDictT) -> List[str]:
    urls: List[str] = []

    for page in start_pages:
        if isinstance(page, dict):
            url = _build_url_from_dict(page, options)
        else:
            url = _build_url_from_string(page, options)
        urls.append(url)

    return urls


def open(start_pages: Iterable[Union[str, Dict[str, str]]], options: OptionsDictT) -> None:
    # Build full URLs for starting pages (including host and port)
    start_urls = _build_urls(start_pages, options)
    
    mode = options.get('mode')
    if not isinstance(mode, (str, bool, type(None))) or mode is True:
        raise TypeError("'mode' option must by either a string, False, or None")
    if mode is None or mode is False:
        # Don't open a browser
        pass
    elif mode == 'custom':
        # Just run whatever command the user provided
        if not isinstance(options['cmdline_args'], list):
            raise TypeError("'cmdline_args' option must be of type List[str]")
        sps.Popen(options['cmdline_args'],
                  stdout=sps.PIPE, stderr=sps.PIPE, stdin=sps.PIPE)
    elif mode in _browser_modules:
        # Run with a specific browser
        browser_module = _browser_modules[mode]
        path = _browser_paths.get(mode)
        if path is None:
            # Don't know this browser's path, try and find it ourselves
            path = browser_module.find_path()
            _browser_paths[mode] = path

        if path is not None:
            browser_module.run(path, options, start_urls)
        else:
            raise EnvironmentError("Can't find %s installation" % browser_module.name)
    else:
        # Fall back to system default browser
        for url in start_urls:
            wbr.open(url)


def set_path(browser_name: str, path: str) -> None:
    _browser_paths[browser_name] = path


def get_path(browser_name: str) -> Optional[str]:
    return _browser_paths.get(browser_name)

