# Scrapy settings for scraper project

BOT_NAME = "scraper"

SPIDER_MODULES = ["scraper.spiders"]
NEWSPIDER_MODULE = "scraper.spiders"

# Use Playwright
DOWNLOADER_MIDDLEWARES = {
    "scrapy_playwright.middlewares.ScrapyPlaywrightMiddleware": 543,
}

PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_LAUNCH_OPTIONS = {"headless": True}

# Other settings
ROBOTSTXT_OBEY = False
FEEDS = {
    "output.json": {
        "format": "json",
        "overwrite": True,
    },
}
