# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    authors = scrapy.Field()
    main_price = scrapy.Field()
    sale_price = scrapy.Field()
    currency = scrapy.Field()
    url = scrapy.Field()
    rating = scrapy.Field()
    _id = scrapy.Field()
