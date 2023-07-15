import scrapy
from bookscraper.items import BookItem


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]    # specifically scrape domain and ignore links to other websites
    start_urls = ["https://books.toscrape.com"]

    # Determine where data will be saved / this overides settings.py
    custom_settings = {
        'FEEDS':{
            'spider_generated_bookdata.json': {'format': 'json' , 'overwrite': True},
        }
    }

    # Grab all the books from the main page
    def parse(self, response):
        books = response.css('article.product_pod')

        # Goes to individual book based on url and parses specific content with function parse_book_page
        # Loops to the next book until it parses all books on the current page
        for book in books:
            relative_url = response.css('h3 a ::attr(href)').get()         # link to individual book

            if 'catalogue/' in relative_url:
                next_page_url = 'https://books.toscrape.com/' + relative_url
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + relative_url
            yield response.follow(next_page_url, callback=self.parse_book_page)

        # Goes to next page after parsing all content of each book on current page
        next_page = response.css('li.next a ::attr(href)').get()

        if next_page is not None:
            if 'catalogue/' in next_page:
                book_url = 'https://books.toscrape.com/' + next_page
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(book_url, callback=self.parse)


    # Parsing specific information from the page of individual book
    def parse_book_page(self, response):
        table_rows = response.css("table tr")
        book_item = BookItem()

        book_item['url'] = response.url,
        book_item['title'] = response.css('.product_main h1::text').get(),
        book_item['upc'] = table_rows[0].css('td ::text').get(),
        book_item['product_type'] = table_rows[1].css('td ::text').get(),
        book_item['price_excl_tax'] = table_rows[2].css('td ::text').get(),
        book_item['price_incl_tax'] = table_rows[3].css('td ::text').get(),
        book_item['tax'] = table_rows[4].css('td ::text').get(),
        book_item['availability'] = table_rows[5].css('td ::text').get(),
        book_item['num_reviews'] = table_rows[6].css('td ::text').get(),
        book_item['stars'] = response.css("p.star-rating").attrib['class'],
        book_item['category'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
        book_item['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
        book_item['price'] = response.css('p.price_color ::text').get(),

        yield book_item

        # pass

# command used to scrape ---- scrapy crawl bookspider -o bookdata.json