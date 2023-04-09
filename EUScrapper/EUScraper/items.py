# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()

class FileItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()

class Item(scrapy.Item):
    parent_url = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    article_index = scrapy.Field()
    published_on = scrapy.Field()
    body = scrapy.Field()

    file_urls = scrapy.Field()
    files = scrapy.Field()

    image_urls = scrapy.Field()
    images = scrapy.Field()