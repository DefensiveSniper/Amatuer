const { app, BrowserWindow, Menu, shell } = require('electron'); 
const path = require('path');
const { spawn } = require('child_process');

let flaskProcess;

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 700,
    icon: path.join(__dirname, 'static', 'images', 'logo.ico'),
    webPreferences: {
      nodeIntegration: false, 
    }
  });

  const checkServer = () => {
    fetch('http://127.0.0.1:6969')
      .then(() => win.loadURL('http://127.0.0.1:6969'))
      .catch(() => setTimeout(checkServer, 1000));
  };

  checkServer();
}

app.whenReady().then(() => {
    Menu.setApplicationMenu(null); 
    
    let flaskPath;
    if (process.env.NODE_ENV === "development") {
        flaskPath = path.join(__dirname, 'main.exe'); // 开发模式
    } else {
        flaskPath = path.join(process.resourcesPath, '..', 'main.exe'); // 生产模式
    }

    flaskProcess = spawn(flaskPath, { detached: true, stdio: 'ignore' });
    flaskProcess.unref();

    createWindow();

    app.on('activate', function () {
      if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') {
    if (flaskProcess) flaskProcess.kill();
    app.quit();
  }
});
