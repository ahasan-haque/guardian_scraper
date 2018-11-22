import scrapy
from datetime import datetime
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags


class GuardianItem(scrapy.Item):
    """
    Fields passed from spider are pre/postprocessed here
    """
    headline = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    author = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    content = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join('\n')
    )
    category = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    sub_category = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    creation_date = scrapy.Field(
        output_processor=TakeFirst()
    )