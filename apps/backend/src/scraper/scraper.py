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

    return event_urls


def main():
    previous_events = set()
    run_time = 0

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            while run_time < 3600:  # 1時間（3600秒）でループを停止
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

                run_time += 3600

    except Exception as e:
        print(f"エラーが発生しました: {e}")

    finally:
        browser.close()  # ブラウザを閉じる


if __name__ == "__main__":
    main()
