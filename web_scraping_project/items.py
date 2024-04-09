import scrapy

# Item class for Spider1
class Spider1Item(scrapy.Item):
    time_posted = scrapy.Field()
    url_of_topic = scrapy.Field()
    title_topic = scrapy.Field()
    user = scrapy.Field()
    comments_count = scrapy.Field()

# Item class for Spider2
class Spider2Item(scrapy.Item):
    time_posted = scrapy.Field()
    url_of_topic = scrapy.Field()
    title_topic = scrapy.Field()
    user = scrapy.Field()
    page_url = scrapy.Field()
    comment = scrapy.Field()

