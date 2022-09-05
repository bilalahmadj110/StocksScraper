import requests
import pandas as pd
from constants import AVAILABLE_MODES, URL1, CSV1, KEEP_ONLY_1
from alerts import log, success

SCRAPPER = "1"


def stock_numbers(mode, csv=CSV1):
    try:
        url = URL1.format(mode=mode)
        log(SCRAPPER, f"Loading URL {url}", 0)

        # load request
        r = requests.get(url)
        if r.status_code != 200:
            log(SCRAPPER, f"Unreachable host. status-code: {r.status_code}", 1)
            return False

        log(SCRAPPER, "Loading HTML.", 0)
        table = pd.read_html(r.text)
        df = table[0]
        df = df[2:].reset_index().rename(columns=df.iloc[0])
        del df['index']
        # df.columns = df.iloc[0]
        log(SCRAPPER, "Filtering columns", 0)
        #
        # keeping only the necessary columns and deleting all others
        for col in df.columns:
            if col in KEEP_ONLY_1:
                continue
            del df[col]
        # df[['有價證券代號', '名稱']] = df["有價證券代號及名稱"].str.split(" ", 1, expand=True)
        log(SCRAPPER, f"Exporting to csv {csv.format(mode=mode)}", 0)
        df.to_csv(csv.format(mode=mode), index=False, encoding="utf_8_sig")
        success(SCRAPPER, f"Compiled Successfully!")
        return csv


    except Exception as e:
        log(SCRAPPER, f"Exception, failed to run {str(e)}", 1)
        return False


def start_scraping():
    for strMode in AVAILABLE_MODES:
        stock_numbers(strMode)


if __name__ == "__main__":
    start_scraping()
