# scraper.py
import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# 公式サイトのURL
url = "https://talent.supporterz.jp/geekcamp/"


def get_hackathon_events(page):
    # Webページを読み込む
    page.goto(url)
    page.wait_for_timeout(3000)

    # PlaywrightとBeautifulSoupでHTMLを解析
    content = page.content()
    soup = BeautifulSoup(content, "html.parser")

    # イベント情報を取得（ex：イベントリストのクラスが "event-item" の場合）
    events = soup.find_all("div", class_="event-item")

    event_urls = []
    for event in events:
        link = event.find("a", href=True)
        if link:
            event_urls.append(link["href"])
