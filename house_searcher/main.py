import sqlite3
import time
import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import splinter

# Set up logging
logger = logging.getLogger("searcher_app")
logger.setLevel(logging.DEBUG)

fileHandler1 = logging.FileHandler("searcher_DEBUG.log")
fileHandler1.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fileHandler1.setFormatter(formatter)
consoleHandler.setFormatter(formatter)

logger.addHandler(fileHandler1)
logger.addHandler(consoleHandler)

class HouseSpider:

    def __init__(self):
        executable_path = {'executable_path':"D:/Programmas/ChromeDriver/chromedriver.exe"}
        browser = splinter.Browser(driver_name='chrome', user_agent= "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36", **executable_path)
        self.driver = browser.driver
        self.driver.get("https://www.immoweb.be/nl/immo/appartement/te-koop")

        # Set up header of browser
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

        # Set up connection with database
        conn = sqlite3.connect("searcher.db")
        # cursor = conn.cursor()

        self._add_postcodes()

    def _add_postcodes(self):
        postcodes = ["2000", "2018", "2020", "2030","2040","2050","2060","2070"]
        for code in postcodes:
            try:
                elem = self.driver.find_element_by_id("localisation")
                #elem.click()
                time.sleep(0.8)
                elem.send_keys(code)
            except Exception as e:
                logger.error("Unable to add " + code + " to the location input box.")
                logger.error(e)
        
        try:
            elem = self.driver.find_element_by_id("localisation")
            elem.click()
        except Exception as e:
            logger.error("Unable to click the search button.")
            logger.error(e)
            exit()

    def _try_click(self, xpath):
        try:
            logger.debug("Trying to click: " + xpath)
            elem = self.driver.find_element_by_xpath(xpath)
            elem.click()
        except:
            logger.error("Unable to click: " + xpath)
            return False
        return True


if __name__ == "__main__":
    spider = HouseSpider()