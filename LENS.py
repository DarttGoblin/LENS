from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()
driver.get("https://www.theguardian.com/world/israel")
time.sleep(3)

soup = BeautifulSoup(driver.page_source, "lxml")
links = [a["href"] for a in soup.find_all("a", class_="dcr-2yd10d", href=True)]
articles = []

for link in links[:5]:  # limit to 5 for testing
    driver.get(link)
    time.sleep(2)
    
    page = BeautifulSoup(driver.page_source, "lxml")
    
    # Extract main title
    title_tag = page.find("h1")
    title = title_tag.text.strip() if title_tag else None
    
    # Extract subtitle (standfirst / intro)
    subtitle_tag = page.find("div", {"class": "dcr-185kyl0"})
    subtitle = subtitle_tag.text.strip() if subtitle_tag else None
    
    # Extract body paragraphs
    body_paras = [p.text.strip() for p in page.find_all("p", {"class": "dcr-130mj7b"})]
    
    articles.append({
        "url": link,
        "title": title,
        "subtitle": subtitle,
        "body": " ".join(body_paras)
    })

driver.quit()

# Show result
for a in articles:
    print(a["title"])
    print(a["subtitle"])
    print(a["body"][:200], "...\n")  # preview
