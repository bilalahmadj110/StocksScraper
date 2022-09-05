from datetime import datetime, timedelta
import time
import pytz

tz = pytz.timezone('Asia/Taipei')

now = datetime.now(tz=tz)
timestamp = int(datetime.timestamp(now) * 1000)

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

""" SCRAPER 3"""
today3 = now.strftime(f"{now.year - 1911}/%m/%d")
URL3 = f"https://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_result.php?l=zh-tw&d={today3}&se=EW&_={timestamp}"
CSV3 = "stock-after-trading.csv"
KEEP_ONLY_3 = (0, 2,)
