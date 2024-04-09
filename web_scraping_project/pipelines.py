from bs4 import BeautifulSoup
import mysql.connector
from itemadapter import ItemAdapter
from datetime import datetime

class WebScrapingProjectPipeline:
    def process_item(self, item, spider):
        # Clean up 'time' field
        item['time_posted'] = item['time_posted'].replace('T', ' ')
        if item.get('url_of_topic', '').startswith('item'): # Clean up 'url_of_topic' field and append preffix
            item['url_of_topic'] = 'https://news.ycombinator.com/' + item['url_of_topic']
        
        
        item['comments_count'] = int(item['comments_count'].split('\xa0')[0]) # Delete word comments and convert number to integer

        return item
    
class WebScrapingProjectPipeline2:
    def process_item(self, item, spider):
        # Clean time_posted
        item['time_posted'] = item['time_posted'].replace('T', ' ') # Delete word T
        
        # Append prefix to page_url
        if 'page_url' in item:
            item['page_url'] = self.append_prefix(item['page_url']) 

        # Clean up 'url_of_topic' field and append preffix 
        if item.get('url_of_topic', '').startswith('item'): 
            item['url_of_topic'] = 'https://news.ycombinator.com/' + item['url_of_topic']
        
        return item
    
    def append_prefix(self, url):
        prefix = 'https://news.ycombinator.com/'
        return prefix + url

# Responsible for storing Spider1's extracted data into a MySQL database
class Spider1DatabasePipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()
    
    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  #add your password here if you have one set
            database=''   #add your database
        )
        self.curr = self.conn.cursor()
    
    def create_table(self):
        self.curr.execute("""
                          CREATE TABLE IF NOT EXISTS data (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            title_topic VARCHAR(255) NOT NULL,
                            url_of_topic VARCHAR(255),
                            time_posted DATETIME,
                            comments_count INTEGER,
                            user VARCHAR(255)
                        )
                        """)
        self.conn.commit()
    
    def process_item(self, item, spider):
        self.store_db(item)
        return item
    
    def store_db(self, item):
        sql_query = """
            INSERT INTO data (title_topic, url_of_topic, time_posted, comments_count, user) 
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            item['title_topic'],
            item['url_of_topic'],
            item['time_posted'],
            item['comments_count'],
            item['user']
        )

        self.curr.execute(sql_query, values)
        self.conn.commit()

    def close(self):
        if self.curr:
            self.curr.close()
        if self.conn:
            self.conn.close()

# Responsible for storing Spider2's extracted data into a MySQL database
class Spider2DatabasePipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()
    
    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='', #add your password here if you have one set
            database=''  #add your database 
        )
        self.curr = self.conn.cursor()
    
    def create_table(self):
        self.curr.execute("""CREATE TABLE IF NOT EXISTS comments (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            title_topic VARCHAR(255) NOT NULL,
                            url_of_topic VARCHAR(255),
                            user VARCHAR(255),
                            comment TEXT,
                            time_posted DATETIME,
                            page_url VARCHAR(255)
                        )
            """)
        self.conn.commit()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        query = """
                INSERT INTO comments (title_topic, url_of_topic, user, comment, time_posted, page_url)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
        values = (
            item['title_topic'],
            item['url_of_topic'],
            item['user'],
            item['comment'],
            item['time_posted'],
            item['page_url']
        )
        self.curr.execute(query, values)
        self.conn.commit()


    def close(self):
        if self.curr:
            self.curr.close()
        if self.conn:
            self.conn.close()