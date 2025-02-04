const { app, BrowserWindow, Menu, shell } = require('electron'); // 确保 shell 正确引入
const path = require('path');

function createWindow() {
  // 创建一个浏览器窗口
  const win = new BrowserWindow({
    width: 1200,
    height: 700,
    // 指定图标（针对 Windows / Linux）
    icon: path.join(__dirname, 'static', 'images', 'logo.ico'),
    webPreferences: {
      nodeIntegration: false, // 确保安全
    }
  });

  // 加载你的 Python 服务地址
  // 这里的地址要和 Flask 的运行端口保持一致，默认为 http://127.0.0.1:5000
  win.loadURL('http://127.0.0.1:5000');

  // 监听新窗口打开事件，确保外部链接在默认浏览器打开
  win.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url); // 让外部链接用默认浏览器打开
    return { action: 'deny' }; // 阻止 Electron 内部打开
  });
}

// 当 Electron 初始化完成并且可以创建浏览器窗口时，这个方法会被调用
app.whenReady().then(() => {
    Menu.setApplicationMenu(null); // 移除菜单
    createWindow();

    app.on('activate', function () {
      // 在 macOS 上，当单击 dock 图标并且没有其他窗口打开时，
      // 通常在应用程序中重新创建一个窗口。
      if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

// 当所有窗口都被关闭后退出应用 (除非你在 macOS 上用特例处理)
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
