import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]    # specifically scrape domain and ignore links to other websites
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        pass
