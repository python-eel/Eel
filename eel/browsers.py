import webbrowser as wbr
import eel.chrome as chr
import subprocess as sps

def _build_url_from_dict(page, options):
    scheme = page.get('scheme', 'http')
    host = page.get('host', 'localhost')
    port = page.get('port', 8000)
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
    start_urls = _build_urls(start_pages, options)

    if options['mode'] in ['chrome', 'chrome-app']:
        chr.run(options, start_urls)
    elif options['mode'] in [None, False]:
        pass  # Don't open a browser
    elif options['mode'] == 'custom':
        sps.Popen(options['args'],
                  stdout=sps.PIPE, stderr=sps.PIPE, stdin=sps.PIPE)
    else:
        # Use system default browser
        for url in start_urls:
            wbr.open(url)
