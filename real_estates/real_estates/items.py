# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RealEstateItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    area = scrapy.Field()
    price = scrapy.Field()
    location = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
