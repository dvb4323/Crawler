# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo
import re
from urllib.parse import urlparse

class BatdongsanPipeline:
    def __init__(self):
        self.conn = pymongo.MongoClient('localhost', 27017)
        self.db = self.conn['real_estate_hanoi']
        # self.collection = db['ba_dinh']

    def get_collection_name(self, url):
        parsed_url = urlparse(url)
        path = parsed_url.path

        # Remove .html extension if present
        if path.endswith('.html'):
            path = path[:-5]  # Remove the last 5 characters (.html)

        # Extract relevant parts from the path
        parts = path.split('/')

        # Find the part that starts with 'huyen-' or 'quan-' or similar, assuming they are unique identifiers for the location
        location_part = next((part for part in parts if part.startswith('quan-') or part.startswith('huyen-')),
                             'default_collection')

        # Replace '-' with '_' to form a valid collection name
        collection_name = location_part.replace('-', '_')

        return collection_name if collection_name else 'default_collection'

    def process_item(self, item, spider):
        # self.collection.insert_one(dict(item))
        # return item
        collection_name = self.get_collection_name(spider.crawled_url)
        collection = self.db[collection_name]
        collection.insert_one(dict(item))
        return item