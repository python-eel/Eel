from __future__ import print_function
import sys
import pkg_resources as pkg
import PyInstaller.__main__ as pyi
import os

args = sys.argv[1:]
main_script = args.pop(0)
web_folder = args.pop(0)

print("Building executable with main script '%s' and web folder '%s'...\n" %
      (main_script, web_folder))

eel_js_file = pkg.resource_filename('eel', 'eel.js')
js_file_arg = '%s%seel' % (eel_js_file, os.pathsep)
web_folder_arg = '%s%s%s' % (web_folder, os.pathsep, web_folder)

needed_args = ['--hidden-import', 'bottle_websocket',
               '--add-data', js_file_arg, '--add-data', web_folder_arg]
full_args = [main_script] + needed_args + args

print('Running:\npyinstaller', ' '.join(full_args), '\n')

pyi.run(full_args)
