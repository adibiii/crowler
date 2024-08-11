import sqlite3

import requests
from bs4 import BeautifulSoup

from config import cities, BASE_URL
from crawler import LinkCrawler, DataCrawler, ImageCrawler

#
# conn = sqlite3.connect('craig_list.db')
# conn.execute('''create table links(
#                 url text NOT NULL,
#                 flag integer NOT NULL
#                 );''')
# conn.execute('''create table data(
#                 title text,
#                 price text,
#                 body text,
#                 post_id text,
#                 created_time text
#                 );''')
# # #
# res = requests.get('https://amsterdam.craigslist.org/apa/d/huge-canal-house-bedrooms-bathrooms/7737362530.html')
# #
# soup = BeautifulSoup(res.text)
# a_tags = soup.find('div', class_='swipe-wrap')
# # images = list()
# for t in a_tags.descendants:
#     print(t)

if __name__ == '__main__':
    # a = LinkCrawler(cities, BASE_URL)
    # a.start()
    # b = DataCrawler()
    # b.start()
    c = ImageCrawler()
    c.start()



