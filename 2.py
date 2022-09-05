import pandas as pd
from constants import URL2, CSV2, KEEP_ONLY_2
import requests
from alerts import log, success

SCRAPPER = "2"


def start_scraping(csv=CSV2):
    try:
        log(SCRAPPER, f"Loading URL {URL2}", 0)
        r = requests.get(URL2)
        if r.status_code != 200:
            log(SCRAPPER, f"Unreachable host. status-code: {r.status_code}", 1)
            return False
        log(SCRAPPER, "Loading JSON.", 0)
        json = r.json()
        fields9 = json.get('fields9', None)
        data = json.get('data9', None)

        if fields9 is None or data is None:
            log(SCRAPPER, f"No data retrieved.", 1)
            return False

        log(SCRAPPER, "Filtering rows", 0)
        # filtering rows where len("證券代號") != 4
        data = filter(lambda row: len(row[0]) == 4, data)

        df = pd.DataFrame(data, columns=fields9)
        log(SCRAPPER, "Filtering columns", 0)
        # keeping only the necessary columns and deleting all others
        for col in df.columns:
            if col in KEEP_ONLY_2:
                continue
            del df[col]
        log(SCRAPPER, f"Exporting to csv {csv}", 0)
        df.to_csv(csv, index=False, encoding="utf_8_sig")
        success(SCRAPPER, f"Compiled Successfully!")
        return csv

    except Exception as e:
        log(SCRAPPER, f"Exception, failed to run {str(e)}", 1)
        return False


if __name__ == "__main__":
    start_scraping()
