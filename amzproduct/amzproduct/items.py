# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmzproductItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    seller = scrapy.Field()
    description= scrapy.Field()
    # rate of the item, out of 5
    rating = scrapy.Field()
    # review = scrapy.Field()
    # url of the item page
    url = scrapy.Field()
    # Amazon Standard Identification Number
    asin= scrapy.Field()
    # first image in the item page
    img = scrapy.Field()
    # Date First Available
    firstDate = scrapy.Field()
    # rank in the search results
    rank = scrapy.Field()
    pass

class ReviewItem(scrapy.Item):
    # to identify the same product
    asin = scrapy.Field()
    review_id = scrapy.Field()
    reviewer = scrapy.Field()
    review_url = scrapy.Field()
    star = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    pass
