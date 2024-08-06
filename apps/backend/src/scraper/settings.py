# settings.py

# Playwrightミドルウェアの追加
SPIDER_MIDDLEWARES = {
    "scrapy_playwright.middleware.ScrapyPlaywrightMiddleware": 543,
}

# Playwright設定
PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
}

# その他の設定（必要に応じて追加）
LOG_LEVEL = "INFO"
