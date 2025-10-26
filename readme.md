# 🤖 Bot Search – Buscador Multimarketplaces

O **Bot Search** é uma aplicação desktop desenvolvida com **Electron** e **Python**, criada para **buscar produtos em múltiplos marketplaces** (AliExpress, Made-in-China, 1688 e eBay) de forma **automatizada, visual e controlável em tempo real**.

---

## 🚀 Funcionalidades

✅ Interface amigável em **Electron**  
✅ Busca simultânea em **diversos marketplaces internacionais**  
✅ Exibição **em tempo real** dos logs e resultados no painel  
✅ Botões para **Pausar, Retomar e Finalizar** o processo de busca  
✅ Exportação dos resultados em **CSV** ou **XLSX**  
✅ Processamento paralelo com **ThreadPoolExecutor (Python)**  
✅ Suporte a **vários termos de busca de uma só vez**

---

## 🧠 Arquitetura do Projeto

O projeto combina o poder de **Python para web scraping** com a **interface gráfica moderna do Electron**:

```
bot-search/
├── main.js                     # Código principal do app Electron
├── index.html                  # Interface (frontend)
├── renderer.js (opcional)      # Lógica da interface
├── python/
│   ├── search_marketplaces.py  # Motor de busca (Python)
│   ├── results.csv             # Exportações geradas
│   └── drivers/
│       └── chromedriver.exe    # Driver do Selenium
├── package.json                # Dependências do Electron
└── README.md                   # Este arquivo ✨
```

---

## 🛠️ Pré-requisitos

- [Node.js](https://nodejs.org/) (versão 18+ recomendada)
- [Python 3.9+](https://www.python.org/)
- [Google Chrome](https://www.google.com/chrome/)
- [ChromeDriver compatível](https://chromedriver.chromium.org/downloads)

---

## ⚙️ Instalação

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/seuusuario/bot-search.git
cd bot-search
```

### 2️⃣ Instalar dependências do Electron

```bash
npm install
```

### 3️⃣ Instalar dependências do Python

```bash
cd python
pip install -r requirements.txt
```

**Exemplo de `requirements.txt`:**
```
selenium
beautifulsoup4
lxml
pandas
openpyxl
```

---

## 💻 Uso

### 🔹 Iniciar o app

Na raiz do projeto:

```bash
npm start
```

### 🔹 No aplicativo:
1. Digite os **termos de busca** (exemplo: “drone frame”, “motor brushless”)
2. Clique em **Iniciar busca**
3. Acompanhe o progresso em tempo real no painel
4. Utilize:
   - ⏸️ **Pausar**
   - ▶️ **Retomar**
   - 🛑 **Finalizar**
5. Após a conclusão, clique em **Exportar resultados**  
   para salvar em `.csv` ou `.xlsx`

---

## 📦 Exportação

Os resultados são automaticamente salvos em:

```
python/results.csv
python/results.xlsx
```

Você também pode exportar manualmente pela interface Electron.

---

## 🧩 Tecnologias utilizadas

| Tecnologia | Função |
|-------------|--------|
| **Electron** | Interface desktop (frontend + backend) |
| **Python** | Motor de scraping e exportação |
| **Selenium** | Automação de navegação nos marketplaces |
| **BeautifulSoup4** | Extração e parse de HTML |
| **Pandas** | Manipulação e exportação de dados |
| **Node.js / IPC** | Comunicação entre Electron e Python |

---

## 🧠 Estrutura da Comunicação

O Electron controla o processo Python e transmite logs via **IPC (Inter Process Communication)**:

```
[Electron UI] ⇄ [main.js] ⇄ [Python subprocess]
```

📡 Logs, erros e progresso são enviados em tempo real para a interface.

---

## 📊 Exemplo de Log

```
[INFO] ================= BUSCANDO: Frame (hexacopter) =================
[INFO] [AliExpress] buscando: Frame (hexacopter)
[INFO] [1688] buscando: Frame (hexacopter)
[INFO] [Made-in-China] buscando: Frame (hexacopter)
[INFO] [eBay] buscando: Frame (hexacopter)
[INFO] [aliexpress] retornou 2 itens
[INFO] [madeinchina] retornou 0 itens
🛑 Processo finalizado manualmente.
✅ Busca finalizada (código 0).
```

---

## ⚠️ Observações

- Certifique-se de que o **ChromeDriver** é compatível com sua versão do Chrome.
- Alguns marketplaces podem bloquear o acesso após muitas requisições — o bot respeita intervalos aleatórios entre buscas.
- Caso queira adicionar novos marketplaces, edite o arquivo `search_marketplaces.py` e insira uma nova função de scraping.

---

## 🧰 Futuras melhorias

- [ ] Barra de progresso visual  
- [ ] Salvamento automático incremental  
- [ ] Busca agendada (cron-like)  
- [ ] Histórico de pesquisas  
- [ ] Filtro de resultados duplicados  

---

## 👨‍💻 Autor

Desenvolvido por **Mateus S.**  
💼 Projeto pessoal de automação e análise de marketplaces.

📬 Contato: [seu-email@exemplo.com](mailto:seu-email@exemplo.com)

---

## 🧾 Licença

Este projeto é distribuído sob a licença **MIT**.  
Sinta-se à vontade para usar, modificar e contribuir!
