import subprocess as sps
import sys

def run(options, start_urls):
    # TODO: this properly
    cmd = ['C:\\Users\\Chris\\Coding\\Algojammer\\node_modules\\electron\\dist\\electron.exe']
    cmd += options['cmdline_args']
    cmd += ['.', ';'.join(start_urls)]
    sps.Popen(cmd, stdout=sys.stdout, stderr=sps.PIPE, stdin=sps.PIPE)

def get_instance_path():
    if sys.platform in ['win32', 'win64']:
        return find_electron_win()
    elif sys.platform == 'darwin':
        return find_electron_mac()
    elif sys.platform.startswith('linux'):
        return find_electron_linux()
    else:
        return None

def find_electron_win():
    import winreg as reg
    reg_path = r'Software\Classes\electron-api-demos\shell\open\command'
    for install_type in reg.HKEY_CURRENT_USER, reg.HKEY_LOCAL_MACHINE:
        try:
            reg_key = reg.OpenKey(install_type, reg_path, 0, reg.KEY_READ)
            electron_path = reg.QueryValue(reg_key, None)
            reg_key.Close()
        except WindowsError:
            electron_path = None
        else:
            break

    return electron_path
