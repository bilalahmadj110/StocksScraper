import pandas as pd
from selenium import webdriver
import os
from bs4 import BeautifulSoup as soup
import requests
from alerts import log, success
import psutil

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from constants import URL4, INPUT_TXT, RESP_TABLE, URL4_MAIN, CURRENT_WORKING_DIRECTORY

SCRAPPER = "4"

chrome_options = Options()
if os.name != 'nt':
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
else:
    os.chdir(CURRENT_WORKING_DIRECTORY)
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()


class FinancialStatements:

    @staticmethod
    def check_if_running():
        global driver
        driver_process = psutil.Process(driver.service.process.pid)
        if not driver_process.is_running():
            driver = webdriver.Chrome(options=chrome_options)
            driver.maximize_window()

    def scrape(self, stock_num):  # 1
        self.create(str(stock_num))
        log(SCRAPPER, f">> {stock_num}", 0)
        # always checks t
        self.check_if_running()
        log(SCRAPPER, f"Loading URL {URL4}", 0)
        if driver.current_url != URL4:
            driver.get(URL4)
        wait = WebDriverWait(driver, 15)
        elem = wait.until(EC.presence_of_element_located((By.XPATH, INPUT_TXT)))
        elem.clear()
        elem.send_keys(stock_num)
        elem.send_keys(Keys.ENTER)

        elem = wait.until(EC.presence_of_element_located((By.XPATH, RESP_TABLE)))
        src = elem.get_attribute('innerHTML')
        self.scrape_urls(str(stock_num), src)

    @staticmethod
    def create(dir_):
        if not os.path.exists(dir_):
            os.mkdir(dir_)

    def scrape_tables(self, stock_num, year_name, url):  # 3
        d = os.path.join(stock_num, year_name)
        self.create(d)
        log(SCRAPPER, f"   Loading URL {url}", 0)
        r = requests.get(url)
        if r.status_code != 200:
            log(SCRAPPER, f"   ERROR: Unreachable host. status-code: {r.status_code}", 1)
            return False
        src = soup(r.content, "html.parser")
        tables = src.find_all("table")
        log(SCRAPPER, f"   Total {len(tables)} table(s) found.", 0)
        for index, table in enumerate(tables):
            log(SCRAPPER, f"   Scraping table {index + 1} of {len(tables)}.", 1)
            try:
                table = pd.read_html(str(table))[0]
                table.to_csv(os.path.join(d, f"{table.columns[0][0]}.csv"), index=False, encoding="utf_8_sig")
            except (ValueError, IndexError) as ve:
                log(SCRAPPER, f"   ERROR: failed to retrieve table at position {index + 1}.", 0)
                with open(f"table_{index}.html", "w", encoding="utf_8_sig") as f:
                    f.write(str(table))

    @staticmethod
    def parse_url(onclick):
        try:
            s = onclick.replace('window.open(\'', '')
            return URL4_MAIN + s.split('\',')[0]
        except Exception as ignore:
            return None

    def scrape_urls(self, stock_num, src):  # 2
        """
        This function scrapes the URLs for the next page for difference years.
        Also, further calls the next scraper [scrape_tables]  on each year.
        We can limit this to only few years.

        :param stock_num:
        :param src:
        :return:
        """
        tables = soup(src, "html.parser")
        rows = tables.find("table").find("tbody").find_all("tr")

        for row in rows[2:][:2]:
            cells = row.find_all("td")
            year_name = cells[0].text
            url = self.parse_url(cells[2].find('input')['onclick'])
            log(SCRAPPER, f"  Scraping year `{year_name}`...", 1)
            self.scrape_tables(stock_num, year_name, url)

    def __enter__(self):
        self.check_if_running()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        try:
            driver.close()
        except:
            pass


if __name__ == "__main__":
    with FinancialStatements() as fs:
        fs.scrape(1104)
        fs.scrape(1102)
