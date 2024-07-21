import scrapy


class QuotestoscrapeSpider(scrapy.Spider):
    name = "quotestoscrape"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    max_follow = 1

    def parse(self, response):
        rows = response.xpath('//div[@class="quote"]')
        for row in rows:
            text = row.xpath('.//span[@class="text"]/text()').get().strip('“').strip('”')
            author = row.xpath('.//small[@class="author"]/text()').get().strip()

            yield {
                'text': text,
                'author': author
            }

        next_page_btn = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page_btn and self.max_follow:
            self.max_follow -= 1
            yield response.follow(next_page_btn,callback=self.parse)


