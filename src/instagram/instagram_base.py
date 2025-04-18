from ..facebook.scraper import Scraper
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from config import Config as config
from ..logs import Logs

logs = Logs()


class BaseInstagramScraper(Scraper):
    def __init__(self, user_id: str, base_url: str) -> None:
        super().__init__()
        self._user_id = user_id
        self._base_url = base_url.format(self._user_id)
        options = self._chrome_driver_configuration()
        options.add_argument("--headless=new")
        self._driver = webdriver.Chrome(options=options)
        self._driver.get(self._base_url)
        self._wait = WebDriverWait(self._driver, 10)
        self.success = False
