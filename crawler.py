import lib
from multiprocessing import Pool
from multiprocessing import freeze_support

crawl_list = lib.create_list_crawler('div.tileItem', { 'title': 'h2.tileHeadline', 'link': 'a.url' }, 'div#parent-fieldname-text')

def crawl_list_wrapper(index):
    url = f'https://kommunikation.uni-freiburg.de/pm/pressemitteilungen?b_start:int={index}'
    return crawl_list(url)

if __name__ == '__main__':
    freeze_support()

    with Pool(10) as p:
        items = p.map(crawl_list_wrapper, range(0, 2420, 20))
