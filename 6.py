import time
from alerts import log, success
import pandas as pd
import psutil
from io import StringIO

import requests
import os
import pandas as pd
import io
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from constants import URL6, CURRENT_WORKING_DIRECTORY, DATE_PATH6, STOCK_PATH6, TABLE6, LINK6

SCRAPPER = "6"

chrome_options = Options()
if os.name != 'nt':
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
else:
    os.chdir(CURRENT_WORKING_DIRECTORY)
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,ur;q=0.8,pa;q=0.7,ar;q=0.6',
    'Connection': 'keep-alive',
    'Host': 'smart.tdcc.com.tw',
    'Referer': 'https://www.tdcc.com.tw/',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}


class ScrapeHoldings:

    @staticmethod
    def check_if_running():
        global driver
        driver_process = psutil.Process(driver.service.process.pid)
        if not driver_process.is_running():
            driver = webdriver.Chrome(options=chrome_options)
            driver.maximize_window()

    def scrape(self, stock_num, date):
        self.stock_num = stock_num
        self.date = date
        self.check_if_running()
        log(SCRAPPER, f"Scraping {stock_num=} {date=} - {URL6}")
        driver.get(URL6)
        wait = WebDriverWait(driver, 15)
        select = Select(driver.find_element(By.XPATH, DATE_PATH6))
        # select by visible text
        select.select_by_visible_text(date)
        elem = wait.until(EC.presence_of_element_located((By.XPATH, STOCK_PATH6)))
        elem.send_keys(str(stock_num))
        time.sleep(1)
        elem.send_keys(Keys.ENTER)
        self.scrape_table(driver.page_source)
        self.download_csv(driver.page_source)
        success(SCRAPPER, f"  {self.stock_num=} {self.date=}")

    def scrape_table(self, src):
        log(SCRAPPER, "  Scraping table")
        soup = BeautifulSoup(src, 'html.parser')
        table_src = soup.find("div", {"class": TABLE6}).find("table")
        df = pd.read_html(str(table_src))[0]
        log(SCRAPPER, "  Table retrieved")
        df.to_csv(f"scrape_holding_table_{self.stock_num}_{self.date}", index=False, encoding="utf_8_sig")

    def mkdirs(self, stock_num):
        if not os.path.exists("ScrapeHoldings"):
            os.mkdir("ScrapeHoldings")
        if not os.path.exists(os.path.join("ScrapeHoldings", str(stock_num))):
            os.mkdir(os.path.join("ScrapeHoldings", str(stock_num)))
        if not os.path.exists(os.path.join("ScrapeHoldings", str(stock_num))):
            os.mkdir(os.path.join("ScrapeHoldings", str(stock_num)))


    def download_csv(self, src):
        log(SCRAPPER, "  Scraping csv link")
        soup = BeautifulSoup(src, 'html.parser')
        link = soup.find("a", {"title": LINK6})['href']
        log(SCRAPPER, f"  Link retrieved {link}")
        s = requests.get(link, headers=HEADERS).text
        c = pd.read_csv(StringIO(s))
        c.to_csv(f"scrape_holding_csv_{self.stock_num}_{self.date}", index=False, encoding="utf_8_sig")


if __name__ == '__main__':
    ScrapeHoldings().scrape("1101", "20220624")
    try:
        driver.quit()
    except:
        pass
