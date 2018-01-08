import sys, pkg_resources as pkg, PyInstaller.__main__ as pyi, os

eel_js_file = pkg.resource_filename('eel', 'eel.js')
js_file_arg = '%s%seel' % (eel_js_file, os.pathsep)
needed_args = ['--hidden-import', 'bottle_websocket', '--add-data', js_file_arg]

pyi.run(sys.argv[1:] + needed_args)
