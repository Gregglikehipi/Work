from bs4 import BeautifulSoup
import requests


class Crawler:

    def get_html(self, url):
        return BeautifulSoup(requests.get(url).text, 'html.parser')