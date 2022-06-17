import requests
from bs4 import BeautifulSoup
from newspaper import Article
from tqdm import tqdm
import pandas as pd


class PcGamer:
    page_news_links = []

    def __init__(self):
        self.domain = 'https://pcgamer.com'
        self.base_url = 'https://pcgamer.com/news/'
        self.page_number = 1
        self.current_page_url = 'https://pcgamer.com/news/'
        self.current_page_html = None
        self.contents = []

    def next_page(self):
        self.page_number += 1
        self.current_page_url = self.base_url + 'page/' + str(self.page_number) + '/'

    def add_links(self, page_count: int):
        for i in tqdm(range(page_count)):
            self.current_page_html = requests.get(self.current_page_url).text
            soup = BeautifulSoup(self.current_page_html, features='html.parser')
            # print(self.current_page_html)
            divs = soup.find_all('div', {'class': "listingResult"})
            for div in divs:
                try:
                    self.page_news_links.append(div.a['href'])
                except:
                    pass

            self.next_page()

    def get_content(self):
        for link in tqdm(self.page_news_links):
            try:
                article = Article(link)
                article.download()
                article.parse()
                self.contents.append(article.text)
            except Exception as e:
                pass

    def write_csv(self):
        fd = pd.DataFrame(self.contents)
        fd.to_csv('PcGamer_news.csv')


pc_gamer = PcGamer()
pc_gamer.add_links(page_count=1)
pc_gamer.get_content()
pc_gamer.write_csv()
