import requests
from bs4 import BeautifulSoup
from alerts import log, success

from constants import URL5, CLICK_ME_MAIN, CATEGORIES5, URL5_MAIN, CSV_DOWNLOAD_5

SCRAPPER = "5"


class StockRevenue:
    headers = {'Accept-Language': 'en-US,en;q=0.9,ur;q=0.8,pa;q=0.7,ar;q=0.6',
               'Accept-Encoding': 'gzip, deflate, br',
               'Sec-Fetch-Site': 'same-origin', 'Host': 'mops.twse.com.tw',
               'Accept': '*/*',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/106.0.0.0 Safari/537.36',
               'Connection': 'keep-alive',
               'Sec-Fetch-Mode': 'cors',
               'sec-ch-ua-platform': '"Windows"', 'sec-ch-ua-mobile': '?0',
               'Content-Type': 'application/x-www-form-urlencoded',
               'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
               'Sec-Fetch-Dest': 'empty'}
    body = {
        "step": "1",
        "firstin": "1",
        "off": "1",
        "TYPEK": None,
        "year": None,
        "month": None
    }

    def __init__(self, years, months):
        for body in self.encodeFormData(years, months):
            if 'Sec-Fetch-Dest' in self.headers:
                del self.headers['Sec-Fetch-Dest']
            f_page = self.post_main(body)
            if not f_page:
                continue
            url_s_page = self.parse_main(f_page)
            if url_s_page is None:
                continue
            s_content = self.get_second(url_s_page)
            if not s_content:
                continue
            name = self.parse_csv_page(s_content)
            if not name:
                continue
            b = self.gen_body_csv(name, s_content)
            if not b:
                continue
            # at this point we've a URL and body for requesting CSV. Lets request CSV
            self.download_csv(CSV_DOWNLOAD_5, b, body['TYPEK'], body['year'], body['month'])
            success(SCRAPPER,
                    f"Successfully retrieved csv for type={body['TYPEK']}, year={body['year'],}, month={body['month']}")
            # break

    def download_csv(self, url, payload, type_, year, month):
        log(SCRAPPER, f"Downloading CSV {url}...")
        self.headers['Sec-Fetch-Dest'] = 'document'
        response = requests.post(url, data=payload, headers=self.headers)
        if response.status_code != 200:
            log(SCRAPPER, f"  ERROR: failed to download CSV!")
        data = response.content
        with open(f'stock_revenue_{type_}_{year}_{month}.csv', 'wb') as s:
            s.write(data)

    # post values to the main page
    def post_main(self, payload):
        log(SCRAPPER,
            f"Loading URL {URL5} params[m={self.body['month']}, y={self.body['year']}, typek={self.body['TYPEK']}]", 0)
        r = requests.post(URL5, headers=self.headers, data=payload)
        if r.status_code != 200:
            log(SCRAPPER, f"  Error: Failed to load page with error code -> {r.status_code}", 0)
            return None
        return r.content

    def get_second(self, url):
        log(SCRAPPER, f"Loading s_URL {url}", 0)
        r = requests.get(url, headers=self.headers)
        if r.status_code != 200:
            log(SCRAPPER, f"  Error: Failed to load page with error code -> {r.status_code}", 0)
            return None
        return r.content

    # get next page url from main page
    def parse_main(self, content):
        log(SCRAPPER, f"  Parsing first page", 0)
        soup = BeautifulSoup(content, 'html.parser')
        btn = soup.find('input', {'value': CLICK_ME_MAIN})
        if btn is None:
            log(SCRAPPER, f"  Error: Couldn't scrape next page url from the main page", 0)
            return btn
        return self.parse_url(btn.findParent('form')['onsubmit'])

    # get the second page csv button
    def parse_csv_page(self, content):
        log(SCRAPPER, f"  Parsing second page", 0)
        soup = BeautifulSoup(content, 'html.parser')
        btn = soup.find('input', {'type': "button"})
        if btn is None:
            log(SCRAPPER, f"  Error: Couldn't scrape csv url from the second page.", 0)
            return None
        return self.parse_csv_name(btn['onclick'])

    def encodeFormData(self, years, months):
        for c in CATEGORIES5:
            for year in years:
                for month in months:
                    self.body['month'] = '%02d' % month
                    self.body['year'] = "%d" % year
                    self.body['TYPEK'] = c
                    yield self.body

    @staticmethod
    def parse_url(onclick):
        try:
            s = onclick.replace('window.open(\'', '').replace("','');return false;", "")
            return URL5_MAIN + s.split('\',')[0]
        except (AttributeError, ValueError, IndexError):
            return None

    @staticmethod
    def parse_csv_name(path):
        try:
            return path.split('=')[1].split('"')[1]
        except (AttributeError, ValueError, IndexError):
            return None

    @staticmethod
    def gen_body_csv(name, s_content):
        log(SCRAPPER, f"  Generating body for csv request.", 0)
        soup = BeautifulSoup(s_content, 'html.parser')
        form = soup.find('form', {"action": "/server-java/FileDownLoad"})
        body = {}
        for inputs in form.find_all("input"):
            body[inputs['name']] = inputs['value']
        if not body:
            log(SCRAPPER, f"  Error: Couldn't scrape csv body for request from the second page.", 0)
            return None
        body['fileName'] = name
        return body


if __name__ == '__main__':
    StockRevenue([111], [1])
