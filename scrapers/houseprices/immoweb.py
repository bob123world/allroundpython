import logging
import json
import platform
import os
import sys
import time
import splinter
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

class Immoweb():
    def __init__(self, config):
        self.soup = None
        if "immoweb" not in config:
            logger.critical("example not defined in config.json!")
            exit()
            if "url" not in config["immoweb"]:
                logger.critical("url not defined under example in config.json!")
                exit()

        ### create driver
        try:
            # driver_path = os.path.join(config["root"], "chromedriver", "chromedriver.exe")
            executable_path = {'executable_path': os.path.join(config["root"], "chromedriver", "chromedriver.exe")}

            browser = splinter.Browser(driver_name='chrome', user_agent= "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36", **executable_path)
            self.driver = browser.driver
            logger.info("Driver initialized!")

        except Exception as e:
            logger.critical("Unable to create the driver, with error message: " + str(e))

        
        ### create data folder
        self.data_folder = os.path.join(config["root"], "data")
        self.create_folder(self.data_folder)
        self.data_folder = os.path.join(self.data_folder, "example")
        self.create_folder(self.data_folder)

        ### Get google and save the webpage
        self.driver.get(config["example"]["url"])
        self.scroll()
        self.save_webpage(os.path.join(self.data_folder, "nieuwsblad.html"))

        ### Close the driver
        self.driver.close()
        
    def create_folder(self, folder):
        """create a folder"""
        try:
            if not os.path.exists(folder):
                os.mkdir(folder)
        
        except Exception as e:
            logger.error(e)

    def save_webpage(self, path):
        """Save the content of a webpage"""
        try:
            with open(path, "w") as f:
                f.write(self.driver.page_source)
        
        except Exception as e:
            logger.error(e)


    # helper function: used to scroll the page
    def scroll(self):
        """Scroll help function that scrolls to the bottom of the page"""
        current_scrolls = 0

        while True:
            try:
                if current_scrolls == 50:
                    return

                old_height = self.driver.execute_script("return document.body.scrollHeight")
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.01)
                current_scrolls += 1
            except Exception as e:
                logger.error(e)
                break

        return

    def _try_click(self, xpath):
        """Try clicking on a specific xpath element"""
        try:
            logger.debug("Trying to click: " + xpath)
            elem = self.driver.find_element_by_xpath(xpath)
            elem.click()
        except:
            logger.error("Unable to click: " + xpath)
            return False
        return True

    



if __name__ == "__main__":
    # Set up logging
    logger = logging.getLogger("immoweb-scraper")
    logger.setLevel(logging.DEBUG)
    fileHandler1 = logging.FileHandler("immoweb-scraper.log")
    fileHandler1.setLevel(logging.DEBUG)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fileHandler1.setFormatter(formatter)
    consoleHandler.setFormatter(formatter)

    logger.addHandler(fileHandler1)
    logger.addHandler(consoleHandler)

    try:
        root_folder_name = "scrapers"
        root = os.path.abspath(__file__)
        while root_folder_name not in root[-len(root_folder_name):]:
            root = os.path.dirname(root)

        with open(os.path.join(root,"config.json"), "r") as file:
            config = json.load(file)

        config["root"] = root

    except Exception as e:
        logger.critical("Unable to find config.json at following path: " + str(os.path.join(root,"config.json")))
        exit()

    spider = immoweb(config)