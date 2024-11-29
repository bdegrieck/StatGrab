import requests
from bs4 import BeautifulSoup

from Backend.errors import InvalidResponse


class Scraper:
    """
    Scraper is a tool for web scraping sites
    url - url site
    """

    def __init__(self, url: str):
        self.url = url

    @property
    def grab(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            raise InvalidResponse(response=response.status_code, url=self.url)
        scraper = BeautifulSoup(response.content, "html.parser")
        return scraper







