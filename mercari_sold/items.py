# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MercariSoldItem(scrapy.Item):
    title = scrapy.Field()
    categories = scrapy.Field()
    price = scrapy.Field()
    shipping_fee = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
