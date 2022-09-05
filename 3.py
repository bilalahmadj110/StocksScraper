import pandas as pd
from constants import URL3, CSV3, KEEP_ONLY_3
import requests
from alerts import log, success

SCRAPPER = "3"


def start_scraping(csv=CSV3):
    try:
        log(SCRAPPER, f"Loading URL {URL3}", 0)
        r = requests.get(URL3)
        if r.status_code != 200:
            log(SCRAPPER, f"Unreachable host. status-code: {r.status_code}", 1)
            return False
        log(SCRAPPER, "Loading JSON.", 0)
        json = r.json()
        data = json.get("aaData", None)

        if data is None or len(data) == 0:
            log(SCRAPPER, f"No data retrieved.", 1)
            return False

        log(SCRAPPER, "Filtering rows", 0)
        # filtering rows where len("證券代號") != 4
        data = filter(lambda row: len(row[0]) == 4, data)

        df = pd.DataFrame(data)

        log(SCRAPPER, "Filtering columns", 0)
        # keeping only the necessary columns and deleting all others
        for index, col in enumerate(df.columns):
            if index in KEEP_ONLY_3:
                continue
            del df[col]

        df.columns = ["代號", "收盤"]
        log(SCRAPPER, f"Exporting to csv {csv}", 0)
        df.to_csv(csv, index=False, encoding="utf_8_sig")
        success(SCRAPPER, f"Compiled Successfully!")
        return csv

    except Exception as e:
        log(SCRAPPER, f"Exception, failed to run {str(e)}", 1)
        return False


if __name__ == "__main__":
    start_scraping()
