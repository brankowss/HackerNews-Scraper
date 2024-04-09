import scrapy
from web_scraping_project.items import Spider1Item

class Spider1Spider(scrapy.Spider):
    name = "spider1"
    allowed_domains = ["news.ycombinator.com"]
    start_urls = ["https://news.ycombinator.com/"]

    custom_settings = {
    'FEED_EXPORT_FIELDS': ['title_topic', 'url_of_topic', 'user', 'time_posted', 'comments_count'],
    'ITEM_PIPELINES': {
        'web_scraping_project.pipelines.WebScrapingProjectPipeline': 300,
        'web_scraping_project.pipelines.Spider1DatabasePipeline': 400,
    }}

    def parse(self, response):
        athing = response.xpath('//tr[@class="athing"]') 
        subtext = response.xpath('//td[@class="subtext"]')
        
        for a, s in zip(athing, subtext):    
            item = Spider1Item()
            item['title_topic'] = a.xpath('.//span[@class="titleline"]/a/text()').get()
            item['url_of_topic'] = a.xpath('.//span[@class="titleline"]/a/@href').get()
            item['time_posted'] = s.xpath('.//span[@class="age"]/@title').get()
            item['comments_count'] = s.xpath('.//span[@class="age"]/following-sibling::*[3]/text()').get()
            item['user'] = s.xpath('.//a[@class="hnuser"]/text()').get()
            yield item
    
        next_page = response.xpath('//td[@class="title"]/a/@href').get()

        if next_page is not None:
            next_page_url = 'https://news.ycombinator.com/' + next_page
            yield response.follow(next_page_url, callback=self.parse)
