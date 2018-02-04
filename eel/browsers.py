import webbrowser as wbr, subprocess as sps
from .chrome import Chrome

def open(start_pages, options):
    base_url = 'http://%s:%d/' % (options['host'], options['port'])
    start_urls = [base_url + page for page in start_pages]

    if options['mode'] in ['chrome', 'chrome-app']:
        chrome_path = Chrome().instance 
  
        if chrome_path != None:
            if options['mode'] == 'chrome-app':
                for url in start_urls:
                    sps.Popen([chrome_path, '--app=%s' % url] + options['chromeFlags'], stdout=sps.PIPE, stderr=sps.PIPE)
            else:
                args = options['chromeFlags'] + start_urls
                sps.Popen([chrome_path, '--new-window'] + args, stdout=sps.PIPE, stderr=sps.PIPE)
        else:
            raise EnvironmentError("Can't find Chrome or Chromium installation")
    elif options['mode'] in [None, False]:
        pass # Don't open a browser
    else:
        # Use system default browser
        for url in start_urls:
            wbr.open(url)
