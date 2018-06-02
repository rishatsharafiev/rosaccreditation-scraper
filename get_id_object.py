# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
DOTENV_PATH = os.path.join(BASE_PATH, '.env')
load_dotenv(DOTENV_PATH)

import logging, time
import unittest, json
from datetime import datetime
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.common.exceptions import WebDriverException, NoSuchElementException

class TestRosAccreditationSite(unittest.TestCase):

    def setUp(self):
        # initialize logget
        self.logger = logging.getLogger(__name__)
        logger_handler = logging.FileHandler(os.path.join(BASE_PATH, '{}.log'.format(__file__)))
        logger_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        logger_handler.setFormatter(logger_formatter)
        self.logger.addHandler(logger_handler)
        self.logger.setLevel(logging.WARNING)
        self.logger.propagate = False

        # self.display = Display(visible=0, size=(1024,800))
        # self.display.start()

        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.chromedriver_path = os.path.join(self.current_path, 'chromedriver')
        self.driver = webdriver.Chrome(self.chromedriver_path)
        self.write_filename = 'output.csv'

    def test_get_offers_list(self):
        driver = self.driver
        driver.implicitly_wait(15)

        try:
            page_url = 'http://public.fsa.gov.ru/table_rds_pub_ts/'
            driver.get(page_url)
            btn_find = driver.find_element_by_id('btn_find')
            btn_find.click()
            time.sleep(30)
            driver.execute_script('window.tableManager.changePerPage(2000)')
            time.sleep(40)
            links = driver.find_elements_by_css_selector('tr > td:nth-child(2) > a')

            with open('links.json', 'w+') as write_file:
                links = [link.get_attribute('href') for link in links]
                write_file.write(json.dumps(links))

        except Exception as e:
            self.logger.exception(str(e))
        finally:
            driver.quit()


if __name__ == '__main__':
    unittest.main()
