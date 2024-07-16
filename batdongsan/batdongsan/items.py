# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BatdongsanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    road_before_width = scrapy.Field()
    floors = scrapy.Field()
    bedrooms = scrapy.Field()
    parking = scrapy.Field()
    area = scrapy.Field()
    size = scrapy.Field()
    direction = scrapy.Field()
    price = scrapy.Field()
    location = scrapy.Field()
    pass
