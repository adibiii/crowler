import json
from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from advertisemntparser import Parser
from config import STORAGE_TYPE
from storage import SqliteStorage, FileStorage


class CrawlerBase(ABC):
    def __init__(self):
        self.storage = self.__set_storage()

    @staticmethod
    def __set_storage():
        if STORAGE_TYPE == 'sqlite':
            return SqliteStorage()
        return FileStorage()

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def store(self, data, filename):
        pass

    @staticmethod
    def get_page(url):
        try:
            response = requests.get(url)
        except :
            return None
        return response.text


class LinkCrawler(CrawlerBase):
    def __init__(self, cities, base_url):
        super().__init__()
        self.cities = cities
        self.base_url = base_url

    @staticmethod
    def get_links(html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        li_tags = soup.find_all('li', class_='cl-static-search-result')
        links = list()
        for li in li_tags:
            links.append({'url': li.a['href'], 'flag': False})
        return links

    def crawl_city(self, city):
        start = 0
        url = self.base_url.format(city, start)
        all_links = list()
        while True:
            res = self.get_page(url)
            if res is None:
                break
            links = self.get_links(res)
            if links in all_links:
                break
            all_links.append(links)
            start += 1
        all_links2 = list()
        for li in all_links:
            all_links2.extend(li)
        return all_links2

    def start(self, store=True):
        adv_links = list()
        for city in self.cities:
            links = self.crawl_city(city)
            print(f'{city} total advertisement: {len(links)}')
            adv_links.extend(links)
        if store:
            self.store(adv_links, 'links')
        # return adv_links

    def store(self, data, filename):
        self.storage.store(data, filename)


class DataCrawler(CrawlerBase):
    def __init__(self):
        super().__init__()
        self.links = self.__load_links()
        self.parser = Parser()

    def __load_links(self):
        urls = self.storage.load()
        return urls

    def start(self, store=True):
        adv_data_list = list()
        for adv in self.links:
            response = self.get_page(adv[0])
            if response:
                data = self.parser.parse(response)
                adv_data_list.append(data)

        if store:
            self.store(adv_data_list, 'data')
        # return adv_data_list

    def store(self, data, filename):
        self.storage.store(data, filename)


class ImageCrawler(CrawlerBase):
    def __init__(self):
        super().__init__()
        self.links = self.__load_links()

    def __load_links(self):
        urls = self.storage.load()
        return urls

    @staticmethod
    def get_images_link(html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        a_tags = soup.find_all('a', class_='thumb')
        images_link = list()
        for a in a_tags:
            images_link.append(a.img['src'])
        return images_link

    @staticmethod
    def get_image(link):
        try:
            response = requests.get(link, stream=True)
        except:
            return None
        return response

    def start(self):
        counter = 1
        for link in self.links:
            res = self.get_page(link[0])
            images_link = self.get_images_link(res)
            if images_link:
                for src in images_link:
                    img_res = self.get_image(src)
                    self.store(img_res, counter)
                    counter += 1

    def store(self, data, filename):
        with open(f'data/pics/{filename}.jpg', 'ab') as f:
            f.write(data.content)
            for _ in data.iter_content():
                f.write(data.content)
        print(filename)


