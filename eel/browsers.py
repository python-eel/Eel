import webbrowser as wbr, sys, subprocess as sps, os

def open(start_pages, options):
    base_url = 'http://%s:%d/' % (options['host'], options['port'])
    start_urls = [base_url + page for page in start_pages]

    if options['mode'] in ['chrome', 'chrome-app']:
        chrome_path = find_chrome()
  
        if chrome_path != None:
            if options['mode'] == 'chrome-app':
                for url in start_urls:
                    sps.Popen([chrome_path, '--disable-gpu', '--app=%s' % url] + options['chromeFlags'])
            else:
                args = options['chromeFlags'] + start_urls
                sps.Popen([chrome_path, '--disable-gpu', '--new-window'] + args)
        else:
            raise EnvironmentError("Can't find Chrome or Chromium installation")
    elif options['mode'] in [None, False]:
        pass # Don't open a browser
    else:
        # Use system default browser
        for url in start_urls:
            wbr.open(url)

def find_chrome():
    if sys.platform in ['win32', 'win64']:
        return find_chrome_win()
    elif sys.platform == 'darwin':
        return find_chrome_mac()
    elif sys.platform.startswith('linux'):
        return find_chrome_linux()
    else:
        return None

def find_chrome_mac():
    default_dir = r'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    if os.path.exists(default_dir):
        return default_dir
    return None

def find_chrome_linux():
    import shutil as shu
    chrome_names = ['chromium-browser',
                    'chromium',
                    'google-chrome',
                    'google-chrome-stable']

    for name in chrome_names:
        chrome = shu.which(name)
        if chrome is not None:
            return chrome
    return None

def find_chrome_win():
    import winreg as reg
    reg_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe'

    for install_type in reg.HKEY_LOCAL_MACHINE, reg.HKEY_CURRENT_USER:
        try:
            reg_key = reg.OpenKey(install_type, reg_path, 0, reg.KEY_READ)
            chrome_path = reg.QueryValue(reg_key, None)
        except WindowsError:
            pass
        reg_key.Close()

    return chrome_path

