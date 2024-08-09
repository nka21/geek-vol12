import scrapy
from ..items import DynamicScraperItem


class HackathonSpider(scrapy.Spider):
    name = "hackathon"

    def start_requests(self):
        urls = ["https://talent.supporterz.jp/geekcamp/"]

        for url in urls:
            yield scrapy.Request(
                url=url, meta={"playwright": True, "playwright_include_page": True}
            )

    def parse(self, response):
        for event in response.css("#events > div > div.container"):
            event_item = DynamicScraperItem()
            event_item["url"] = event.css("a::attr(href)").get()
            event_item["title"] = event.css(
                "div.container.outer dd:nth-of-type(2)::text"
            ).get()
            yield event_item
