import scrapy


class HackathonSpider(scrapy.Spider):
    name = "hackathon"

    def start_requests(self):
        allowed_domains = ["talent.supporterz.jp"]
        urls = ["https://talent.supporterz.jp/geekcamp/"]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pass
