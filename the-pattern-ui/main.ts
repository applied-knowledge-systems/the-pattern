import { app, BrowserWindow } from "electron";
import * as path from "path";
const url = require("url");

let win: Electron.BrowserWindow;
function createWindow() {
  win = new BrowserWindow({ width: 800, height: 600 });
  // load the dist folder from Angular
  win.loadURL(
    url.format({
      pathname: path.join(__dirname, '/dist/ui/index.html'),
      protocol: "file:",
      slashes: true
    })
  );
  // The following is optional and will open the DevTools:
  // win.webContents.openDevTools()
  win.on("closed", () => {
    win = null;
  });
}
app.on("ready", createWindow);
// on macOS, closing the window doesn't quit the app
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  // On OS X it"s common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (win === null) {
    createWindow();
  }
});