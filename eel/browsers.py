import webbrowser as wbr, sys, subprocess as sps

def open(start_pages, options):    
    base_url = 'http://%s:%d/' % (options['host'], options['port'])
    start_urls = [base_url + page for page in start_pages]
    
    if options['mode'] in ['chrome', 'chrome-app']:
        chrome_path = find_chrome()
        if chrome_path != None:
            if options['mode'] == 'chrome-app':
                for url in start_urls:
                    sps.Popen('%s --app=%s' % (chrome_path, url))
            else:
                sps.Popen('%s --new-window %s' % (chrome_path, ' '.join(start_urls)))
        else:
            print("Can't find Chrome or Chromium, try different mode such as 'default'")
    elif False:
        pass # Firefox
    else:
        # Use system default browser
        for url in start_urls:
            wbr.open(url)

def find_chrome():
    if sys.platform in ['win32', 'win64']:
        return find_chrome_win()
    elif sys.platform == 'darwin':
        return None
    elif sys.platform.startswith('linux'):
        return None
    else:
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
    