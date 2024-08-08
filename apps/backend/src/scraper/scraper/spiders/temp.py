from twisted.internet import reactor
from scrapy import signals
from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy.utils.log import configure_logging
from scrapy_playwright.page import PageMethod
import logging
import os
from bs4 import BeautifulSoup

# ログの設定
log_file = "event_info_scraping.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)


class HackathonSpider(Spider):
    name = "hackathon"
    start_urls = ["https://talent.supporterz.jp/geekcamp/"]
    stop_flag_path = ""  # ストップフラグファイルのパス
    scrape_interval = 3600  # スクレイピング間隔（秒）

    custom_settings = {
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 5,
        "AUTOTHROTTLE_MAX_DELAY": 3600,
        "RETRY_ENABLED": True,
        "RETRY_TIMES": 3,
        "RETRY_HTTP_CODES": [500, 502, 503, 504, 408],
        "LOG_FILE": log_file,
        "LOG_LEVEL": "INFO",
    }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(
                url=url,
                callback=self.parse,
                meta={"playwright": True},  # Playwrightを使うリクエスト
            )

    def parse(self, response):
        if os.path.isfile(self.stop_flag_path):
            logging.info("Stop flag detected. Stopping spider.")
            self.crawler.engine.close_spider(self, "Stop flag file detected")
            return

        try:
            # Playwrightがレンダリングしたページからコンテンツを取得
            page = response.meta.get("playwright_page")
            if page:
                content = page.content()
            else:
                content = response.text

            soup = BeautifulSoup(content, "html.parser")
            events = soup.find_all("div", class_="item_left")
            event_urls = [
                event.find("a", href=True)["href"]
                for event in events
                if event.find("a", href=True)
            ]

            for url in event_urls:
                yield {"event_url": url}

        except Exception as e:
            logging.error(f"Error occurred: {e}")

        finally:
            # 次回のスクレイピングまで待機
            reactor.callLater(
                self.scrape_interval, self.schedule_next_request, response.url
            )

    def schedule_next_request(self, url):
        self.crawler.engine.crawl(
            Request(url=url, callback=self.parse, meta={"playwright": True}), self
        )

    def handle_error(self, failure):
        logging.error(f"Request failed: {failure}")
