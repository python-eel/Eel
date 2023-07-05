const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");
const { channels } = require('../src/shared/constants');

let mainWindow;

function createWindow() {
  console.log("Starting electron...");
  const startUrl = process.env.ELECTRON_START_URL || "http://localhost:8000"; // Replace with your server URL
  console.log("startUrl: ", startUrl);

  mainWindow = new BrowserWindow({ 
    width: 800, 
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: false,
      nodeIntegration: true,
      nodeIntegrationInWorker: true
    },
   });
  mainWindow.loadURL(startUrl);

  mainWindow.webContents.openDevTools();  // Open DevTools - Remove for PRODUCTION.
  mainWindow.on("closed", function () {
    mainWindow = null;
  });
}
app.on("ready", function () {
  createWindow();
});
app.on("window-all-closed", function () {
  if (process.platform !== "darwin") {
    app.quit();
  }
});
app.on("activate", function () {
  if (mainWindow === null) {
    createWindow();
    console.log("startUrl:", startUrl);
  }
});

ipcMain.on(channels.APP_INFO, (event) => {
  event.sender.send(channels.APP_INFO, { 
    appName: app.getName(),
    appVersion: app.getVersion(),
  });
});
