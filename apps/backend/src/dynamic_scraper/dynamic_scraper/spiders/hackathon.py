import scrapy


class HackathonSpider(scrapy.Spider):
    name = "hackathon"
    allowed_domains = ["talent.supporterz.jp"]
    start_urls = ["https://talent.supporterz.jp/geekcamp/"]

    def parse(self, response):
        pass
