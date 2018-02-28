import sys, os

class Chrome:
    def __init__(self):
        self._instance = None

        _hooks = {
                'win32': self._chrome_win,
                'win64': self._chrome_win,
                'darwin': self._chrome_mac,
                'linux': self._chrome_linux,
        }

        for key, f in _hooks.items():
            if key in sys.platform:
                self._instance = f() 
                

    @property
    def instance(self):
        return self._instance

    def _chrome_win(self):
        import winreg as reg
        reg_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe'

        for install_type in reg.HKEY_LOCAL_MACHINE, reg.HKEY_CURRENT_USER:
            try:
                reg_key = reg.OpenKey(install_type, reg_path, 0, reg.KEY_READ)
                chrome_path = reg.QueryValue(reg_key, None)
                reg_key.Close()
            except WindowsError:
                chrome_path = None
            

        return chrome_path

    def _chrome_linux(self):
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

    def _chrome_mac(self):
        default_dir = r'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        if os.path.exists(default_dir):
            return default_dir
        return None

