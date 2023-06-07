import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]    # specifically scrape domain and ignore links to other websites
    start_urls = ["https://books.toscrape.com"]


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

        yield{
            'url' : response.url,
            'title' : response.css('.product_main h1::text').get(),
            'product_type' : table_rows[1].css('td ::text').get(),
            'price_excl_tax' : table_rows[2].css('td ::text').get(),
            'price_incl_tax' : table_rows[3].css('td ::text').get(),
            'tax' : table_rows[4].css('td ::text').get(),
            'availability' : table_rows[5].css('td ::text').get(),
            'num_reviews' : table_rows[6].css('td ::text').get(),
            'stars': response.css("p.star-rating").attrib['class'],
            'category' : response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
            'description' : response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
            'price' : response.css('p.price_color ::text').get(),
        }

        # pass

# command used to scrape ---- scrapy crawl bookspider -o bookdata.json