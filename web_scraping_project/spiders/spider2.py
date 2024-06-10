import scrapy
from web_scraping_project.items import Spider2Item

class Spider2Spider(scrapy.Spider):
    name = "spider2"
    allowed_domains = ["news.ycombinator.com"]
    start_urls = ["https://news.ycombinator.com/"]

    custom_settings = {
    'FEED_EXPORT_FIELDS': ['title_topic', 'url_of_topic', 'user', 'comment', 'time_posted', 'page_url'],
    'ITEM_PIPELINES': {
        'web_scraping_project.pipelines.WebScrapingProjectPipeline2': 500,
        'web_scraping_project.pipelines.Spider2DatabasePipeline': 600,
    }
    }

    def parse(self, response):
        urls = response.xpath('//span[@class="age"]/following-sibling::*[3]/@href')
        for url in urls:
            yield response.follow(url.get(), callback=self.parse_comment_page)
    
            next_page = response.xpath('//td[@class="title"]/a/@href').get()
            if next_page is not None:
                next_page_url = 'https://news.ycombinator.com/' + next_page
                yield response.follow(next_page_url, callback=self.parse)
                
    def parse_comment_page(self, response):
        title_text = response.xpath('//span[@class="titleline"]/a/text()').get()
        topic_url = response.xpath('//span[@class="titleline"]/a/@href').get()
        td = response.xpath('//td[@class="default"]')
        for t in td:
            item = Spider2Item()
            item['title_topic'] = title_text
            item['url_of_topic'] = topic_url
            item['user'] = t.xpath('.//span[@class="comhead"]/a/text()').get()
            item['time_posted'] = t.xpath('.//span[@class="age"]/@title').get()
            item['page_url'] = t.xpath('.//span[@class="age"]/a/@href').get()
            
            # List to store comment texts
            comment_texts = []

            # List of possible class names for comment elements
            comment_class_names = ['commtext c00', 'commtext c88', 'commtext c5a', 'commtext c55', 'commtext cce', 'commtext c73', 'commtext c9c', 
                                   'commtext cae', 'commtext cbe', 'commtext cdd']

            # Set to store unique comment texts
            comment_texts = set()

            # Loop through each possible class name
            for class_name in comment_class_names:
                # Fetch text directly from the <span> element with the current class name
                commtext_elements = t.xpath(f'.//span[contains(@class, "{class_name}")]')
                for commtext_element in commtext_elements:
                    commtext_text = commtext_element.xpath('.//text()').get().strip()
                    comment_texts.add(commtext_text)

                    # Fetch text and href attributes from all <a> tags within the <span> element with the current class name
                    for a_element in commtext_element.xpath('.//a'):
                        a_text = a_element.xpath('string()').get().strip()
                        href_attribute = a_element.xpath('@href').get()
                        combined_text = f"{a_text} ({href_attribute})"
                        comment_texts.add(combined_text)

            # Join all unique comment texts into a single string and assign it to the 'comment' field of the item
            item['comment'] = ' '.join(comment_texts)
            yield item


