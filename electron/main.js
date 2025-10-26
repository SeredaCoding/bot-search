const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let pythonProcess;
let paused = false;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1000,
    height: 700,
    webPreferences: { nodeIntegration: true, contextIsolation: false },
  });

  mainWindow.loadFile(path.join(__dirname, 'index.html'));
}

app.whenReady().then(createWindow);

// 🟢 Inicia o script Python
ipcMain.on('run-search', (event, keywords) => {
  const scriptPath = path.join(__dirname, '../python/search_marketplaces.py');
  pythonProcess = spawn('python', [scriptPath, ...keywords]);

  pythonProcess.stdout.on('data', data => {
    mainWindow.webContents.send('search-output', data.toString().trim());
  });

  pythonProcess.stderr.on('data', data => {
  mainWindow.webContents.send('search-output', data.toString().trim());
    });

    pythonProcess.stdout.on('data', data => {
    mainWindow.webContents.send('search-output', data.toString().trim());
    });

  pythonProcess.on('close', code => {
    mainWindow.webContents.send('search-finished', `Busca finalizada (código ${code}).`);
  });
});

let pauseRequested = false;

// ⏸️ Pausar
ipcMain.on('pause-search', () => {
  if (pythonProcess && !pauseRequested) {
    pauseRequested = true;
    mainWindow.webContents.send('search-output', '⏸️ Pausando após a busca atual...');
  }
});

// ▶️ Retomar
ipcMain.on('resume-search', () => {
  if (pauseRequested) {
    pauseRequested = false;
    mainWindow.webContents.send('search-output', '▶️ Busca retomada.');
  }
});


// 🛑 Finalizar
ipcMain.on('stop-search', () => {
  if (pythonProcess) {
    pythonProcess.kill();
    pythonProcess = null;
    mainWindow.webContents.send('search-output', '🛑 Processo finalizado manualmente.');
  }
});

// 💾 Exportar resultados
ipcMain.on('export-results', async () => {
  const fs = require('fs');
  const resultsPath = path.join(__dirname, '../python/results.csv');

  if (!fs.existsSync(resultsPath)) {
    mainWindow.webContents.send('search-error', '⚠️ Nenhum resultado para exportar ainda.');
    return;
  }

  const savePath = dialog.showSaveDialogSync({
    title: 'Salvar resultados',
    defaultPath: 'resultados.csv',
    filters: [{ name: 'CSV Files', extensions: ['csv'] }]
  });

  if (savePath) {
    fs.copyFileSync(resultsPath, savePath);
    mainWindow.webContents.send('search-output', `💾 Arquivo exportado para: ${savePath}`);
  }
});
