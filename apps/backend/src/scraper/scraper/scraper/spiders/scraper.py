import scrapy
from scrapy.http import Request
import logging
from bs4 import BeautifulSoup

# ログの設定
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class HackathonSpider(scrapy.Spider):
    name = "hackathon"
    start_urls = ["https://talent.supporterz.jp/geekcamp/"]

    async def parse(self, response):
        page = response.meta["playwright_page"]
        try:
            await page.wait_for_selector("div.event-item", timeout=10000)
            content = await page.content()

            # BeautifulSoupで解析
            soup = BeautifulSoup(content, "html.parser")

            # イベント情報を取得
            events = soup.find_all(
                "div", class_="event-item"
            )  # class_= ""に追跡したいクラスを入れる

            event_urls = [
                event.find("a", href=True)["href"]
                for event in events
                if event.find("a", href=True)
            ]

            for url in event_urls:
                yield {"event_url": url}

        except Exception as e:
            logging.error(f"エラーが発生しました: {e}")

        finally:
            # ページを再度リクエストして再チェック
            yield Request(
                url=response.url, callback=self.parse, meta={"playwright": True}
            )
