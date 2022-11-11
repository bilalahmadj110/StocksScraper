from datetime import datetime
import pytz

CURRENT_WORKING_DIRECTORY = r"C:\Users\Bilal Ahmad"

tz = pytz.timezone('Asia/Taipei')

now = datetime.now(tz=tz)
timestamp = int(datetime.timestamp(now))

""" SCRAPER 1 """
AVAILABLE_MODES = [2, 4]
URL1 = "https://isin.twse.com.tw/isin/C_public.jsp?strMode={mode}"
CSV1 = "c-public-{mode}.csv"
KEEP_ONLY_1 = ("有價證券代號及名稱", '市場別', '產業別',)

""" SCRAPER 2 """
today = now.strftime("%Y%m%d")
URL2 = f"https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date={today}&type=ALLBUT0999&_={timestamp}"
CSV2 = "trading-exchange.csv"
KEEP_ONLY_2 = ("證券代號", "收盤價",)

""" SCRAPER 3 """
today3 = now.strftime(f"{now.year - 1911}/%m/%d")
URL3 = f"https://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_result.php?l=zh-tw&d={today3}&se=EW&_={timestamp}"
CSV3 = "stock-after-trading.csv"
KEEP_ONLY_3 = (0, 2,)

""" SCRAPER 4 """
URL4_MAIN = "https://mops.twse.com.tw"
URL4 = "https://mops.twse.com.tw/mops/web/t203sb01"
INPUT_TXT = '//*[@id="co_id"]'
RESP_TABLE = '//*[@id="fm1"]'

""" SCRAPER 5 """
URL5_MAIN = "https://mops.twse.com.tw"
URL5 = "https://mops.twse.com.tw/mops/web/ajax_t21sc04_ifrs"
CLICK_ME_MAIN = "請點選這裡"
CATEGORIES5 = ['otc0', "sii0"]
CSV_DOWNLOAD_5 = 'https://mops.twse.com.tw/server-java/FileDownLoad'

""" SCRAPER 6"""
URL6 = "https://www.tdcc.com.tw/portal/zh/smWeb/qryStock"
DATE_PATH6 = '//*[@id="scaDate"]'
STOCK_PATH6 = '//*[@id="StockNo"]'
TABLE6 = 'table-frame securities-overview m-t-20'
LINK6 = "下載股權分散表.csv"

""" SCRAPER 7 """
URL7 = "https://mops.twse.com.tw/mops/web/ajax_stapap1"
