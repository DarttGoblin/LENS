from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import time
import os


def scrape_guardian():
    print("Starting Guardian scraping...")
    guardien_link = "https://www.theguardian.com/world/israel"
    driver = webdriver.Chrome()
    driver.get(guardien_link)
    print("Guardian homepage loaded")
    time.sleep(3)

    guardien_soup = BeautifulSoup(driver.page_source, "lxml")
    guardien_base_url = "https://www.theguardian.com"
    guardien_links = [urljoin(guardien_base_url, a["href"]) for a in guardien_soup.find_all("a", class_="dcr-2yd10d", href=True)]
    print(f"Found {len(guardien_links)} Guardian article links")

    guardien_articles = []
    for i, link in enumerate(guardien_links[:20], start=1):
        print(f"Scraping Guardian article {i}: {link}")
        driver.get(link)
        time.sleep(2)
        page = BeautifulSoup(driver.page_source, "lxml")
        title_tag = page.find("h1")
        subtitle_tag = page.find("div", {"data-gu-name": "standfirst"})
        body_paras = [p.get_text(strip=True) for p in page.select("div[data-gu-name='body'] p")]

        guardien_articles.append({
            "url": link,
            "title": title_tag.text.strip() if title_tag else None,
            "subtitle": subtitle_tag.text.strip() if subtitle_tag else None,
            "body": " ".join(body_paras)
        })

    driver.quit()
    print("Finished Guardian scraping\n")
    return guardien_articles


def scrape_aljazeera():
    print("Starting Al Jazeera scraping...")
    aljazera_link = "https://www.aljazeera.com/middle-east/"
    driver = webdriver.Chrome()
    driver.get(aljazera_link)
    print("Al Jazeera homepage loaded")
    time.sleep(3)

    aljazeera_soup = BeautifulSoup(driver.page_source, "lxml")
    aljazeera_base_url = "https://www.aljazeera.com"
    aljazeera_links = [urljoin(aljazeera_base_url, a["href"]) for a in aljazeera_soup.find_all("a", class_="u-clickable-card__link article-card__link", href=True)]
    print(f"Found {len(aljazeera_links)} Al Jazeera article links")

    aljazeera_articles = []
    for i, link in enumerate(aljazeera_links[:20], start=1):
        print(f"Scraping Al Jazeera article {i}: {link}")
        driver.get(link)
        time.sleep(2)
        page = BeautifulSoup(driver.page_source, "lxml")
        title_tag = page.find("h1")
        subtitle_tag = page.find("p", {"class": "article__subhead"})
        texts = [p.get_text(strip=True) for p in page.select("div.wysiwyg--all-content p, div.article-p-wrapper p")]

        aljazeera_articles.append({
            "url": link,
            "title": title_tag.text.strip() if title_tag else None,
            "subtitle": subtitle_tag.text.strip() if subtitle_tag else None,
            "body": " ".join(texts)
        })

    driver.quit()
    print("Finished Al Jazeera scraping\n")
    return aljazeera_articles


print("=== Starting scraper ===")
guardian_articles = scrape_guardian()
aljazeera_articles = scrape_aljazeera()

print("Saving results to Excel...")
os.makedirs("data", exist_ok=True)
pd.DataFrame(guardian_articles).to_excel("data/guardian_articles.xlsx", index=False)
pd.DataFrame(aljazeera_articles).to_excel("data/aljazeera_articles.xlsx", index=False)
print("Scraping complete. Files saved in /data/")
