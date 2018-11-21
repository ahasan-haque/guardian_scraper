import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags


class GuardianItem(scrapy.Item):
    headline = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    category = scrapy.Field()
    sub_category = scrapy.Field()
    url = scrapy.Field()
    creation_date = scrapy.Field()