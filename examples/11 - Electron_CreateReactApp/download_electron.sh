# Download Electron from url
curl -L -o electronZip.zip https://github.com/electron/electron/releases/download/v24.6.0/electron-v24.6.0-mas-x64.zip
# curl -L -o electronZip.zip https://github.com/electron/electron/releases/download/v24.6.0/electron-v24.6.0-mas-arm64.zip

# Unzip the downloaded Electron build
mkdir electronRelease
unzip electronZip.zip -d electronRelease

# Fix Alias issue
cd electronRelease/Electron.app/Contents/Frameworks/Electron\ Framework.framework

# Replace the aliases with originals
rm -r Libraries
rm -r Resources
rm Electron\ Framework
cd Versions/A
mv Libraries ../../
mv Resources ../../
mv Electron\ Framework ../../


# Return to the top directory
cd ../../../../../../../
rm electronZip.zip

mv electronRelease/Electron.app ./Electron.app
rm -r electronRelease