# HackerNews Scraper

## Overview

This is is simple scraper that uses Scrapy, a powerful web scraping framework in Python, to extract data from a **hackernews** website. The scraping process is divided into two spiders: Spider1 scrapes the main page for key information, while Spider2 follows links on the main page to gather additional details such as comments from individual articles. Both spiders saving the data to **MySQL database**.

## Setup Instructions

To run this project, you'll need to have Python and Scrapy installed on your system. You can install Python from [python.org](https://www.python.org/downloads/) and Scrapy using pip:
```
pip install scrapy
```
To use this code from start to end, follow these steps:

Clone this repository to your local machine using the following command:
```
git clone https://github.com/brankowss/HackerNews-Scraper
cd web-scraping-project
```
Install virtualenv to create a virtual environment for your project. 
If you don't have virtualenv installed, you can install it using pip:
```
pip install virtualenv
```
Create a virtual environment for your project using the following command:
```
virtualenv venv
```
Activate the Virtual Environment:

On Windows, use the following command:
```
venv\Scripts\activate
```
On Unix or MacOS, use:
```
source venv/bin/activate
```
Install the required dependencies for the project using the requirements.txt file:
```
pip install -r requirements.txt
```
This will install Scrapy, BeautifulSoup4 for cleaning, MySQL connector, and other required packages.

## Project Structure

```
.
├── README.md
├── requirements.txt
├── scrapy.cfg
└── web_scraping_project
    ├── __init__.py
    ├── items.py
    ├── middlewares.py
    ├── pipelines.py
    ├── settings.py
    └── spiders
        ├── __init__.py
        ├── spider1.py
        └── spider2.py
```
## Items

### Spider1 Fields

| Field Name    | Description                                   |
|---------------|-----------------------------------------------|
| title_topic   | The title of the topic.                      |
| url_of_topic  | The URL of the topic.                        |
| time_posted   | The time when the topic was posted.          |
| user          | The user who posted the topic.               |
| comments_count| The number of comments on the topic.         |

### Spider2 Fields

| Field Name    | Description                                   |
|---------------|-----------------------------------------------|
| title_topic   | The title of the topic.                      |
| url_of_topic  | The URL of the topic.                        |
| time_posted   | The time the comment was posted.         |
| user          | The user who posted the comment.               |
| comment       | The comment text.                   |
| page_url      | The URL of the page containing the comments.  |

## Pipeline

This project's pipeline is responsible for processing the items scraped by the spider and saving them to a MySQL database using mysql.connector.
Once an item has been populated with data by the spider, it is passed to the pipeline for processing. The pipeline first applies cleaning logic to the item to prepare it for storage. After cleaning, the pipeline establishes a connection to the MySQL database using mysql.connector and inserts the processed data into the corresponding table. For Spider1, the pipeline will save the data to a table named "data" in the MySQL database. For Spider2, the pipeline will save the data to a table named "comments" in the MySQL database.

## Spider

Run Spider1 to scrape the main page and save data to MySQL database:

scrapy crawl spider1

Run Spider2 to scrape comments from all articles and save data to MySQL database:

scrapy crawl spider2

## Scrapy Statistics

**Spider1**
- Number of Items Scraped: 462
- Total Requests Made: 20
- Total Responses Received: 20
- Elapsed Time: 63.81 seconds

**Spider2**
- Number of Items Scraped: 18457
- Total Requests Made: 555
- Total Responses Received: 555
- Elapsed Time: 472.22 seconds

## Additional Notes

- Utilize Scrapy middleware for proxy settings or other custom functionalities.
- This project was made for presenting my web scraping skills and data handling.

## Happy Scraping! 🙂🕷️

