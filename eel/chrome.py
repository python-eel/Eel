import sys, subprocess as sps, os

def run(options, start_urls):
    chrome_path = get_instance_path()

    if chrome_path is not None:
        if options['mode'] == 'chrome-app':
            for url in start_urls:
                sps.Popen([chrome_path, '--app=%s' % url] +
                           options['chromeFlags'],
                           stdout=sps.PIPE, stderr=sps.PIPE, stdin=sps.PIPE)
        else:
            args = options['chromeFlags'] + start_urls
            sps.Popen([chrome_path, '--new-window'] + args,
                       stdout=sps.PIPE, stderr=sps.PIPE, stdin=sps.PIPE)
    else:
        raise EnvironmentError(
            "Can't find Chrome or Chromium installation")


def get_instance_path():
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
    # use mdfind ci to locate Chrome in alternate locations and return the first one
    name = 'Google Chrome.app'
    alternate_dirs = [x for x in sps.check_output(["mdfind", name]).decode().split('\n') if x.endswith(name)] 
    if len(alternate_dirs):
        return alternate_dirs[0] + '/Contents/MacOS/Google Chrome'
    return None


def find_chrome_linux():
    import whichcraft as wch
    chrome_names = ['chromium-browser',
                    'chromium',
                    'google-chrome',
                    'google-chrome-stable']

    for name in chrome_names:
        chrome = wch.which(name)
        if chrome is not None:
            return chrome
    return None


def find_chrome_win():
    import winreg as reg
    reg_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe'

    for install_type in reg.HKEY_CURRENT_USER, reg.HKEY_LOCAL_MACHINE:
        try:
            reg_key = reg.OpenKey(install_type, reg_path, 0, reg.KEY_READ)
            chrome_path = reg.QueryValue(reg_key, None)
            reg_key.Close()
        except WindowsError:
            chrome_path = None
        else:
            break

    return chrome_path
