import scrapy

class CrawlIndexSpider(scrapy.Spider):
    name = "crawl_index"
    start_urls = ["https://data.commoncrawl.org/crawl-data/index.html"]

    def parse(self, response):
        html_content = response.text
        print("[CC] --- FULL HTML CONTENT ---")
        print(html_content)
        print("[CC] --- END HTML CONTENT ---")
        # Bạn có thể tiếp tục parse các link CC-MAIN tại đây

# Để chạy: scrapy runspider crawl_index_spider.py
