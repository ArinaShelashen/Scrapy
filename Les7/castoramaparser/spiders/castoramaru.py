import scrapy
from scrapy.http import HtmlResponse
from castoramaparser.items import CastoramaparserItem
from scrapy.loader import ItemLoader


class CastoramaruSpider(scrapy.Spider):
    name = 'castoramaru'
    allowed_domains = ['castorama.ru']
    start_urls = ['https://www.castorama.ru/decoration/wallpaper']

    def parse(self, response: HtmlResponse):

        next_page = response.xpath("//a[@class='next i-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[contains(@class,'product-card__name')]")
        for link in links:
            yield response.follow(link, callback=self.parse_goods)


    def parse_goods(self, response: HtmlResponse):

        loader = ItemLoader(item=CastoramaparserItem(), response=response)
        loader.add_xpath('name', "//h1[@itemprop='name']/text()")
        loader.add_xpath('price', "//span[@class='regular-price']/span/span/span/text()")
        loader.add_xpath('photo', "//span[@itemprop = 'image']/@content")
        loader.add_value('url', response.url)
        yield loader.load_item()
