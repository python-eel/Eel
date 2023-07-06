rm -r dist/eel_electron_CRA
rm -r build/eel_electron_CRA
rm eel_electron_CRA.spec
npm run build
npm run build-electron
python clean_json.py
python -m eel eel_electron_CRA.py build --add-data 'Electron.app:Electron.app' --add-data 'build/electron:build/electron' --onefile 
# python -m eel eel_electron_CRA.py build --add-data 'Electron.app:Electron.app' --add-data 'build/electron:build/electron' --add-data 'build/package.json:build' --onefile