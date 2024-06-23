from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

from errors import InvalidResponse


@dataclass
class Scraper:
    """

    Scraper is a tool for web scraping sites
    url - url site

    """
    url: str

    def grab(self):
        try:
            response = requests.get(self.url)
            scraper = BeautifulSoup(response.content, "html.parser")

        except:
            raise InvalidResponse(url=self.url, response=response)







