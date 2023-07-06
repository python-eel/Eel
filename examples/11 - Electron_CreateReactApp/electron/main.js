const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");
const { channels } = require("../src/shared/constants");

let mainWindow;
const isMac = process.platform === "darwin";

function createWindow() {
  const startUrl = process.env.ELECTRON_START_URL || "http://localhost:8000"; // Replace with your server URL

  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: false,
      nodeIntegration: true,
      nodeIntegrationInWorker: true,
    },
  });
  mainWindow.loadURL(startUrl);

  mainWindow.on("close", function (e) {
    // Emitted when the window is going to be closed. It's emitted before the beforeunload
    // and unload event of the DOM. Calling event.preventDefault() will cancel the close.
    if (mainWindow) {
      mainWindow.webContents.send("app-close");
    }
  });
  mainWindow.on("closed", function () {
    // Emitted when the window is closed. After you have received this event
    // you should remove the reference to the window and avoid using it any more.
    mainWindow = null;
    app.quit();
  });

  mainWindow.webContents.openDevTools(); // Open the DevTools
}

app.on("ready", createWindow);

app.on("window-all-closed", function () {
  if (!isMac) {
    app.quit();
  }
});

app.on("activate", function () {
  if (mainWindow === null) {
    createWindow();
  }
});

ipcMain.on(channels.APP_INFO, (event) => {
  event.sender.send(channels.APP_INFO, {
    appName: app.getName(),
    appVersion: app.getVersion(),
  });
});