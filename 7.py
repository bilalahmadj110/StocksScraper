import os.path

import pandas as pd

from constants import URL7
import requests
from bs4 import BeautifulSoup
from alerts import log, success

SCRAPPER = "7"
DATA = {'code1': None, 'off': '1', 'TYPEK': 'all', 'isnew': 'true', 'inpuType': 'co_id', 'co_id': '1101',
        'queryName': 'co_id',
        'month': None, 'step': '1', 'year': None, 'checkbtn': None, 'encodeURIComponent': '1', 'firstin': '1',
        'TYPEK2': None,
        'keyword4': None}

HEADERS = {'Accept-Language': 'en-US,en;q=0.9,ur;q=0.8,pa;q=0.7,ar;q=0.6',
           'Accept-Encoding': 'gzip, deflate, br', 'Sec-Fetch-Site': 'same-origin', 'Host': 'mops.twse.com.tw',
           'Accept': '*/*',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
           'Connection': 'keep-alive', 'Cookie': 'jcsession=jHttpSession@6af47f37', 'Sec-Fetch-Mode': 'cors',
           'sec-ch-ua-platform': '"Windows"', 'sec-ch-ua-mobile': '?0',
           'Content-Type': 'application/x-www-form-urlencoded',
           'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"', 'Sec-Fetch-Dest': 'empty'}


class ScrapeDirectors:

    def __init__(self, stock_num, year, month, isnew=True):
        DATA['co_id'] = str(stock_num)
        DATA['month'] = str(month)
        DATA['year'] = str(year)
        DATA['isnew'] = isnew

        resp = self.send_post()
        self.mkdirs(stock_num)
        dfs = self.__scrape_table(stock_num, resp)
        self.export_csvs(stock_num, str(year), str(month), isnew, dfs[0], dfs[1])

    def send_post(self):
        log(SCRAPPER,
            f"Loading URL {URL7} STOCK={DATA['co_id']}, m={DATA['month']}, y={DATA['year']}]", 0)
        r = requests.post(URL7, headers=HEADERS, data=DATA)
        if r.status_code != 200:
            log(SCRAPPER, f"  Error: Failed to load page with error code -> {r.status_code}", 0)
            return None
        return r.content

    def __scrape_table(self, stock_num, html):
        soup = BeautifulSoup(html, 'html.parser')
        tables = soup.find_all('table')
        df = pd.read_html(str(tables[3]))[0]
        df2 = pd.read_html(str(tables[4]))[0]
        return [df, df2]

    def mkdirs(self, stock_num):
        if not os.path.exists("ScrapeDirectors"):
            os.mkdir("ScrapeDirectors")
        if not os.path.exists(os.path.join("ScrapeDirectors", str(stock_num))):
            os.mkdir(os.path.join("ScrapeDirectors", str(stock_num)))
        if not os.path.exists(os.path.join("ScrapeDirectors", str(stock_num))):
            os.mkdir(os.path.join("ScrapeDirectors", str(stock_num)))

    def export_csvs(self, stock_num, y, m, isnew, df1, df2):
        num = 1 if isnew else 2
        p1 = os.path.join(os.path.join("ScrapeDirectors", str(stock_num)), f'table{num}.1 {y}-{m}.csv')
        p2 = os.path.join(os.path.join("ScrapeDirectors", str(stock_num)), f'table{num}.2 {y}-{m}.csv')
        df1.to_csv(p1, index=False, encoding="utf_8_sig")
        df2.to_csv(p2, index=False, encoding="utf_8_sig")
        success(SCRAPPER, f"   Table {num}.1 and {num}.2 are successfully exported to {p1} and {p2} respectively. ")


if __name__ == '__main__':
    ScrapeDirectors(1101, 111, 1)
