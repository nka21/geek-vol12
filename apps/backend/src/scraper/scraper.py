import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os

# 公式サイトのURL
url = "https://talent.supporterz.jp/geekcamp/"

stop_flag_file = "stop_flag.txt"


def get_hackathon_events(page) -> list:
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

    return event_urls


def main():
    previous_events = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # プログラムはバックグラウンドで実行されているので、終了するには終了フラグファイルを作成する。
        try:
            while not os.path.exists(stop_flag_file):
                current_events = set(get_hackathon_events(page))

                # 新しいイベントが追加されているかチェック
                new_events = current_events - previous_events
                if new_events:
                    for event in new_events:
                        print(f"新しいイベントが追加されました: {event}")

                # 前回のイベントリストを更新
                previous_events = current_events

                # 1時間ごとにチェック（3600秒）
                time.sleep(3600)

        finally:
            browser.close()
            if os.path.exists(stop_flag_file):
                os.remove(stop_flag_file)


if __name__ == "__main__":
    main()
