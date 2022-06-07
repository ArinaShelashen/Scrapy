import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem

class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D1%85%D0%B8%D0%BC%D0%B8%D1%8F/?stype=0']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@class="pagination-next__text"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@class="product-title-link"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_book)

    def parse_book(self, response: HtmlResponse):

        url = response.url
        name = response.xpath("//h1/text()").get()
        authors = response.xpath("//a[@data-event-label='author']/text()").getall()
        main_price = response.xpath("//span[@class='buying-price-val-number']/text()").get()
        if not main_price:
            main_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").get()
        sale_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        currency = response.xpath("//span[@class='buying-pricenew-val-currency']/text()").get()
        rating = response.xpath("//div[@id='rate']/text()").get()

        yield BookparserItem(name=name, authors=authors, main_price=main_price, sale_price=sale_price,
                             currency=currency, rating=rating, url=url)

