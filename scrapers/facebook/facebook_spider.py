import logging
import json
import platform
import os
import sys
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class FacebookSpider():
    def __init__(self, config):
        self.soup = None
        if "facebook" not in config:
            logger.critical("facebook not defined in config.json!")
            exit()
            if "email" not in config["facebook"]:
                logger.critical("email not defined under facebook in config.json!")
                exit()
            if "password" not in config["facebook"]:
                logger.critical("password not defined under facebook in config.json!")
                exit()
            if "url" not in config["facebook"]:
                logger.critical("url not defined under facebook in config.json!")
                exit()

        ### create driver
        try:
            # driver_path = os.path.join(config["root"], "chromedriver", "chromedriver.exe")
            executable_path = {'executable_path': os.path.join(config["root"], "chromedriver", "chromedriver.exe")}

            options = Options()

            #  Code to disable notifications pop up of Chrome Browser
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-infobars")
            options.add_argument("--mute-audio")
            
            #browser = splinter.Browser(driver_name='chrome', user_agent= "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36", **executable_path)
            self.driver = webdriver.Chrome(executable_path = os.path.join(config["root"], "chromedriver", "chromedriver.exe"), options = options)
            logger.info("Driver initialized!")

        except Exception as e:
            logger.critical("Unable to create the driver, with error message: " + str(e))

        
        ### create data folder
        self.data_folder = os.path.join(config["root"], "data")
        self.create_folder(self.data_folder)
        self.data_folder = os.path.join(self.data_folder, "facebook")
        self.create_folder(self.data_folder)

        ### Log in to facebook and get the friends of
        self.facebook_login(config["facebook"]["email"], config["facebook"]["password"])
        self.driver.get(config["facebook"]["url"])
        time.sleep(5)
        self.scroll()
        friends = self.driver.find_element_by_xpath(config["facebook"]["friends"])
        #self.save_webpage(os.path.join(self.data_folder, "michael_deboeure_friends_" + datetime.utcnow().strftime("%Y%m%d") + ".txt"))

        results = [x.get_attribute("href") for x in friends]
        results = [self.create_original_link(x) for x in results]

        ### Close the driver
        self.driver.close()

    def facebook_login(self, email, password):
        """Login to facebook using an email and a password"""
        try:
            logger.info("Trying to log in to Facebook")
            self.driver.get("https://facebook.com")
            self.driver.maximize_window()
            self.driver.find_element_by_name("email").send_keys(email)
            self.driver.find_element_by_name("pass").send_keys(password)
            try:
                self.driver.find_element_by_id("loginbutton").click()
            except:
                self.driver.find_element_by_name("login").click()
            logger.info("Logged in to Facebook")
        except Exception as e:
            logger.error(e)

        
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

    def check_height(self, old_height):
        new_height = self.driver.execute_script("return document.body.scrollHeight")
        return new_height != old_height

    # helper function: used to scroll the page
    def scroll(self):
        """Scroll help function that scrolls to the bottom of the page"""
        current_scrolls = 0

        while True:
            try:
                if current_scrolls == 200:
                    return

                old_height = self.driver.execute_script("return document.body.scrollHeight")
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                WebDriverWait(self.driver, 8, 0.05).until(
                    lambda driver: self.check_height(old_height)
                )
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

    def create_original_link(self, url):
        if url.find(".php") != -1:
            original_link = "https://facebook.com" + ((url.split("="))[1])

            if original_link.find("&") != -1:
                original_link = original_link.split("&")[0]

        elif url.find("fnr_t") != -1:
            original_link = ("https://facebook.com" + ((url.split("/"))[-1].split("?")[0]))
        elif url.find("_tab") != -1:
            original_link = ("https://facebook.com" + (url.split("?")[0]).split("/")[-1])
        else:
            original_link = url

        return original_link

    



if __name__ == "__main__":
    # Set up logging
    logger = logging.getLogger("scraper")
    logger.setLevel(logging.DEBUG)
    fileHandler1 = logging.FileHandler("scraper.log")
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

    spider = FacebookSpider(config)