# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WebmdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    drug = scrapy.Field()
    condition = scrapy.Field()
    effectiveness = scrapy.Field()
    ease_of_use = scrapy.Field()
    satisfaction = scrapy.Field()
    comment = scrapy.Field()
    date = scrapy.Field()
    sex = scrapy.Field()
    review = scrapy.Field()
