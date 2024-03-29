# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import hashlib


class BookparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.books

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        h = hashlib.new('sha256')
        h.update(bytes(item['url'], 'utf-8'))
        item['_id'] = h.hexdigest()
        collection.insert_one(item)
        return item
