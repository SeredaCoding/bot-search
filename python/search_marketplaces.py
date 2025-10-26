#!/usr/bin/env python3
"""
search_marketplaces.py
Busca produtos em marketplaces (AliExpress, 1688, Made-in-China, eBay)
"""

import time
import random
import logging
import pandas as pd
from urllib.parse import quote_plus, urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import concurrent.futures
import argparse
import os

# ---------- CONFIGURAÇÃO ----------
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
]
MAX_WORKERS = 4
RATE_MIN = 1.0
RATE_MAX = 2.5
REQUEST_TIMEOUT = 30
CHROME_DRIVER_PATH = os.path.join(os.path.dirname(__file__), "../drivers/chromedriver.exe")

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)

# ---------- HELPERS ----------
def sleep_between():
    time.sleep(random.uniform(RATE_MIN, RATE_MAX))

def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
    driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)
    return driver

# ---------- SCRAPERS ----------
def search_aliexpress(keyword, max_items=10):
    results = []
    url = f"https://www.aliexpress.com/wholesale?SearchText={quote_plus(keyword)}"
    logging.info(f"[AliExpress] buscando: {keyword}")
    try:
        driver = create_driver()
        driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "lxml")
        driver.quit()
        anchors = soup.select("a._3t7zg._2f4Ho") or soup.find_all("a", href=True)
        seen = set()
        for a in anchors:
            if len(results) >= max_items:
                break
            href = a.get("href")
            if not href or href in seen:
                continue
            seen.add(href)
            link = href if href.startswith("http") else urljoin("https://www.aliexpress.com", href)
            title = a.get_text(strip=True) or a.get("title") or ""
            price_span = a.find_next("span")
            price = price_span.get_text(strip=True) if price_span else ""
            results.append({"marketplace": "AliExpress", "title": title, "price": price, "link": link})
    except Exception as e:
        logging.warning(f"Erro AliExpress: {e}")
    return results

def search_ebay(keyword, max_items=10):
    import requests
    results = []
    url = f"https://www.ebay.com/sch/i.html?_nkw={quote_plus(keyword)}"
    logging.info(f"[eBay] buscando: {keyword}")
    try:
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        r = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        soup = BeautifulSoup(r.text, "lxml")
        items = soup.select(".s-item")
        for it in items[:max_items]:
            title_tag = it.select_one(".s-item__title")
            title = title_tag.get_text(strip=True) if title_tag else ""
            link_tag = it.select_one(".s-item__link")
            link = link_tag["href"] if link_tag else ""
            price_tag = it.select_one(".s-item__price")
            price = price_tag.get_text(strip=True) if price_tag else ""
            results.append({"marketplace": "eBay", "title": title, "price": price, "link": link})
    except Exception as e:
        logging.warning(f"Erro eBay: {e}")
    return results

def search_madeinchina(keyword, max_items=10):
    results = []
    url = f"https://www.made-in-china.com/search/?word={quote_plus(keyword)}"
    logging.info(f"[Made-in-China] buscando: {keyword}")
    try:
        driver = create_driver()
        driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "lxml")
        driver.quit()
        cards = soup.select(".products-list .product-item")
        for c in cards[:max_items]:
            a = c.find("a", href=True)
            if not a:
                continue
            link = a["href"]
            if not link.startswith("http"):
                link = urljoin("https://www.made-in-china.com", link)
            title = a.get_text(strip=True)
            price_tag = c.select_one(".price")
            price = price_tag.get_text(strip=True) if price_tag else ""
            results.append({"marketplace": "Made-in-China", "title": title, "price": price, "link": link})
    except Exception as e:
        logging.warning(f"Erro Made-in-China: {e}")
    return results

def search_1688(keyword, max_items=10):
    results = []
    url = f"https://s.1688.com/selloffer/offer_search.htm?keywords={quote_plus(keyword)}"
    logging.info(f"[1688] buscando: {keyword}")
    try:
        driver = create_driver()
        driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "lxml")
        driver.quit()
        anchors = soup.find_all("a", href=True)
        seen = set()
        for a in anchors:
            if len(results) >= max_items:
                break
            href = a.get("href")
            if not href or "offer" not in href or href in seen:
                continue
            seen.add(href)
            link = href if href.startswith("http") else urljoin("https://s.1688.com", href)
            title = a.get_text(strip=True)
            results.append({"marketplace": "1688", "title": title, "price": "", "link": link})
    except Exception as e:
        logging.warning(f"Erro 1688: {e}")
    return results

MARKET_FUNCS = {
    "aliexpress": search_aliexpress,
    "1688": search_1688,
    "madeinchina": search_madeinchina,
    "ebay": search_ebay,
}

def search_all(keyword, marketplaces=None, per_site=5):
    if marketplaces is None:
        marketplaces = list(MARKET_FUNCS.keys())
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(MARKET_FUNCS[m], keyword, per_site): m for m in marketplaces}
        for fut in concurrent.futures.as_completed(futures):
            m = futures[fut]
            try:
                res = fut.result()
                logging.info(f"[{m}] retornou {len(res)} itens")
                results.extend(res)
            except Exception as e:
                logging.warning(f"Erro buscando {m}: {e}")
            sleep_between()
    return results

def main():
    parser = argparse.ArgumentParser(description="Buscar produtos em vários marketplaces")
    parser.add_argument("keywords", nargs="+", help="palavras-chave")
    args = parser.parse_args()

    all_results = []
    for kw in args.keywords:
        logging.info(f"================= BUSCANDO: {kw} =================")
        res = search_all(kw)
        for r in res:
            r["keyword"] = kw
        all_results.extend(res)

    export_results(all_results)
    logging.info("Busca finalizada com sucesso.")

if __name__ == "__main__":
    main()

def export_results(results, out_csv="results.csv", out_xlsx="results.xlsx"):
    if not results:
        logging.info("⚠️ Nenhum resultado para exportar.")
        return

    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, out_csv)
    xlsx_path = os.path.join(base_dir, out_xlsx)

    df = pd.DataFrame(results)
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    df.to_excel(xlsx_path, index=False)

    logging.info(f"✅ Exportado CSV: {csv_path} | XLSX: {xlsx_path}")

