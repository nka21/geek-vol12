import scrapy
from scrapy.http import Request
import logging
from bs4 import BeautifulSoup
import os
import asyncio

# ログの設定
log_file = "hackathon_spider.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)


class HackathonSpider(scrapy.Spider):
    name = "hackathon"
    start_urls = ["https://talent.supporterz.jp/geekcamp/"]
    stop_flag_path = "/path/to/stop_flag"  # ストップフラグファイルのパス
    scrape_interval = 3600  # スクレイピング間隔（秒）

    custom_settings = {
        "AUTOTHROTTLE_ENABLED": True,  # 自動スロットルの有効化
        "AUTOTHROTTLE_START_DELAY": 5,  # 初期のリクエスト遅延
        "AUTOTHROTTLE_MAX_DELAY": 3600,  # 最大遅延時間
        "RETRY_ENABLED": True,  # リトライの有効化
        "RETRY_TIMES": 3,  # リトライ回数
        "RETRY_HTTP_CODES": [
            500,
            502,
            503,
            504,
            408,
        ],  # リトライ対象のHTTPステータスコード
        "LOG_FILE": log_file,  # ログファイルの指定
        "LOG_LEVEL": "INFO",  # ログレベルの指定
    }

    async def parse(self, response):
        # ストップフラグの確認
        if os.path.isfile(self.stop_flag_path):
            logging.info("Stop flag detected. Stopping spider.")
            self.crawler.engine.close_spider(self, "Stop flag file detected")
            return

        # Playwrightページオブジェクトの確認
        page = response.meta.get("playwright_page")
        if page is None:
            logging.error("Playwright page object not found in response meta.")
            return

        try:
            await page.wait_for_selector("div.event-item", timeout=10000)
            content = await page.content()

            # BeautifulSoupで解析
            soup = BeautifulSoup(content, "html.parser")
            events = soup.find_all("div", class_="event-item")
            event_urls = [
                event.find("a", href=True)["href"]
                for event in events
                if event.find("a", href=True)
            ]

            # 新しいイベントのURLを出力
            for url in event_urls:
                yield {"event_url": url}

        except Exception as e:
            logging.error(f"Error occurred: {e}")

        finally:
            # 次回のスクレイピングまで待機
            await asyncio.sleep(self.scrape_interval)
            yield Request(
                url=response.url, callback=self.parse, meta={"playwright": True}
            )
