const { app, BrowserWindow } = require("electron");
const path = require("path");
const url = require("url");

let mainWindow;

function createWindow() {
  console.log("Starting electron...");
  const startUrl = process.env.ELECTRON_START_URL || "http://localhost:8000"; // Replace with your server URL
  console.log("startUrl: ", startUrl);

  mainWindow = new BrowserWindow({ width: 800, height: 600 });
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
