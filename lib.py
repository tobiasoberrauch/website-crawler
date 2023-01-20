from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from os import path
import os
import json
import pandas as pd

class Crawler:
    def __init__(self, crawler_config):
        self.crawler_config = crawler_config

    def crawl(self):
        crawl_list = self.create_list_crawler(
            self.crawler_config['list_selector'], 
            self.crawler_config['items_selector'], 
            self.crawler_config['item_selector']
        )

        items = []
        for index in self.crawler_config['index_loop']:
            url = self.crawler_config['url'](index)
            items.extend(crawl_list(url))
        
        with open('data.json', 'w') as f:
            json.dump(items, f, indent=4)

        df = pd.DataFrame(items)
        df.to_csv('data.csv', index=False, sep=';')

    def create_item_crawler(self, selector):
        def crawl_item(url):
            parsed_url = urlparse(url)
            cache_file = f'data/articles{parsed_url.path}.html'
            cache_dir = path.dirname(cache_file)

            # load cache_file if exists
            if path.exists(cache_file):
                print(f'load article {cache_file}...')
                with open(cache_file, 'r') as f:
                    html = f.read()
            else:
                print(f'crawl article {url}...')
                html = requests.get(url).text

            soup = BeautifulSoup(html, 'html.parser')

            # create folder for cache_file is not exists
            if not path.exists(cache_dir):
                os.makedirs(cache_dir)

            # save raw html
            with open(cache_file, 'w') as f:
                f.write(html)

            try:
                content = soup.select_one(selector).text.strip()
            except:
                content = ''

            return content
        
        return crawl_item

    def create_list_crawler(self, list_selector, items_selector, item_selector):
        def crawl_list(url):
            parsed_url = urlparse(url)
            cache_file = f'data/lists{parsed_url.path}/{parsed_url.query}.html'
            cache_dir = path.dirname(cache_file)

            # load cache_file if exists
            if path.exists(cache_file):
                print(f'load list {cache_file}...')
                with open(cache_file, 'r') as f:
                    html = f.read()
            else:
                print(f'crawl list {url}...')
                html = requests.get(url).text

            soup = BeautifulSoup(html, 'html.parser')

            # create folder for cache_file is not exists
            if not path.exists(cache_dir):
                os.makedirs(cache_dir)

            # save raw html
            with open(cache_file, 'w') as f:
                f.write(html)

            items = []
            # get all div with class .tileItem
            for i in soup.select(list_selector):
                link = i.select_one(items_selector['link'])['href']
                item = {
                    'headline': i.select_one(items_selector['title']).text.strip(),
                    'link': link,
                    'content': self.create_item_crawler(item_selector)(link)
                }
                items.append(item)
            
            return items
        
        return crawl_list