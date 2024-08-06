# scraper.py
import time
from selenium import webdriver
from bs4 import BeautifulSoup

# SeleniumのWebDriver設定（Chromeを使用）
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

url = "https://talent.supporterz.jp/geekcamp/"


def get_hackathon_events():
    # Webページを読み込む
    driver.get(url)
    time.sleep(3)

    # BeautifulSoupで解析
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # イベント情報を取得
    events = soup.find_all(
        "div", class_="event-list"
    )  # ←取得したいクラスに書き換える必要がある。
    event_urls = []

    for event in events:
        link = event.find("a", href=True)
        if link:
            event_urls.append(link["href"])

    return event_urls
