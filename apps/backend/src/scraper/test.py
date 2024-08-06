import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os

# 公式サイトのURL
url = "https://talent.supporterz.jp/geekcamp/"

stop_flag_file = "stop_flag.txt"


def get_hackathon_events(page):
    # Webページを読み込む
    page.goto(url)
    page.wait_for_timeout(3000)

    # PlaywrightとBeautifulSoupでHTMLを解析
    content = page.content()
    soup = BeautifulSoup(content, "html.parser")

    print(content)
