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
        outer_containers = response.css(
            "#events > div > div.container .left.item div.container.outer"
        )

        for outer_container in outer_containers:
            event_item = DynamicScraperItem()
            event_item["url"] = outer_container.css("a::attr(href)").get()
            event_item["title"] = outer_container.css("dd:nth-of-type(2)::text").get()
            yield event_item
