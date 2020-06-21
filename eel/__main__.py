import pkg_resources as pkg
import PyInstaller.__main__ as pyi
import os
from argparse import ArgumentParser

parser = ArgumentParser(description="""
Eel is a little Python library for making simple Electron-like offline HTML/JS GUI apps,
 with full access to Python capabilities and libraries.
""")
parser.add_argument(
    "main_script",
    type=str,
    help="Main python file to run app from"
)
parser.add_argument(
    "web_folder",
    type=str,
    help="Folder including all web files including file as html, css, ico, etc."
)
args, unknown_args = parser.parse_known_args()
main_script = args.main_script
web_folder = args.web_folder

print("Building executable with main script '%s' and web folder '%s'...\n" %
      (main_script, web_folder))

eel_js_file = pkg.resource_filename('eel', 'eel.js')
js_file_arg = '%s%seel' % (eel_js_file, os.pathsep)
web_folder_arg = '%s%s%s' % (web_folder, os.pathsep, web_folder)

needed_args = ['--hidden-import', 'bottle_websocket',
               '--add-data', js_file_arg, '--add-data', web_folder_arg]
full_args = [main_script] + needed_args + unknown_args
print('Running:\npyinstaller', ' '.join(full_args), '\n')

pyi.run(full_args)
