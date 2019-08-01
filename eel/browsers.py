import subprocess as sps
import webbrowser as wbr

import eel.chrome as chm
import eel.electron as ele
import eel.edge as edge
#import eel.firefox as ffx      TODO
#import eel.safari as saf       TODO

_browser_paths = {}
_browser_modules = {'chrome':   chm,
                    'electron': ele,
                    'edge': edge}


def _build_url_from_dict(page, options):
    scheme = page.get('scheme', 'http')
    host = page.get('host', 'localhost')
    port = page.get('port', options["port"])
    path = page.get('path', '')
    return '%s://%s:%d/%s' % (scheme, host, port, path)


def _build_url_from_string(page, options):
    base_url = 'http://%s:%d/' % (options['host'], options['port'])
    return base_url + page


def _build_urls(start_pages, options):
    urls = []

    for page in start_pages:
        method = _build_url_from_dict if isinstance(
            page, dict) else _build_url_from_string
        url = method(page, options)
        urls.append(url)

    return urls


def open(start_pages, options):
    # Build full URLs for starting pages (including host and port)
    start_urls = _build_urls(start_pages, options)
    
    mode = options.get('mode')
    if mode in [None, False]:
        # Don't open a browser
        pass
    elif mode == 'custom':
        # Just run whatever command the user provided
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


def set_path(browser_name, path):
    _browser_paths[browser_name] = path


def get_path(browser_name):
    return _browser_paths.get(browser_name)

