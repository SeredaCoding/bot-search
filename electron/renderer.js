const { ipcRenderer } = require('electron');
const output = document.getElementById('output');

function appendLog(msg) {
  output.textContent += msg + '\n';
  output.scrollTop = output.scrollHeight;
}

document.getElementById('searchBtn').addEventListener('click', () => {
  output.textContent = '';
  const keywords = document.getElementById('keywords').value.split(',').map(k => k.trim());
  if (!keywords[0]) return alert('Digite ao menos uma palavra-chave!');
  ipcRenderer.send('run-search', keywords);
});

document.getElementById('pauseBtn').addEventListener('click', () => ipcRenderer.send('pause-search'));
document.getElementById('resumeBtn').addEventListener('click', () => ipcRenderer.send('resume-search'));
document.getElementById('stopBtn').addEventListener('click', () => ipcRenderer.send('stop-search'));
document.getElementById('exportBtn').addEventListener('click', () => ipcRenderer.send('export-results'));

ipcRenderer.on('search-output', (e, msg) => appendLog(msg));
ipcRenderer.on('search-error', (e, msg) => appendLog('[ERRO] ' + msg));
ipcRenderer.on('search-finished', (e, msg) => appendLog('\n✅ ' + msg));
