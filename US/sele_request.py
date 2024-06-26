from selenium import webdriver
import time, pandas as pd, numpy as np, os
from selenium.webdriver.common.by import By

from dotenv import load_dotenv
from utils import download_pdf, save_data_pkl, load_data_pkl

load_dotenv()
MAIN_URL = "https://resoluciones.uncp.edu.pe/documentos/R-EC"
last_data_path = "./data/last_data.pkl"
local = os.environ.get("LOCAL")


options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.binary_location = "/usr/bin/chromium-browser"


def get_actual_data():
    if local == "1":
        driver = webdriver.Chrome()
    else:
        driver = webdriver.Chrome(options=options)
    driver.get(MAIN_URL)

    time.sleep(1)

    links = driver.find_elements(By.XPATH, "//a[@href]")
    names = driver.find_elements(By.CSS_SELECTOR, "h4")
    dates = driver.find_elements(By.XPATH, "//p[@class='text-muted mb-0']")

    hrefs = [link.get_attribute("href") for link in links]
    pdf_hrefs = [href for href in hrefs if ".pdf" in href]

    names = [name.text for name in names]
    dates = [date.text for date in dates]
    dates = [date.split(":")[1] for date in dates]

    data = {"name": names, "dates": dates, "url_pdf": pdf_hrefs}

    data = pd.DataFrame(data)
    data["dates"] = pd.to_datetime(data["dates"])
    data["name_pdf"] = data["dates"].dt.strftime("%Y_%m_%d")
    # data["name_pdf"] = data["dates"].str.replace(" ", "_") + ".pdf"
    return data


def verify_new_docs():
    last_data = load_data_pkl()
    actual_dates = last_data["dates"].to_numpy()

    data = get_actual_data()
    last_dates = data["dates"].to_numpy()

    exists = np.isin(last_dates, actual_dates, invert=True)

    to_dowload_i = np.where(exists)[0]

    not_downloaded = data.iloc[to_dowload_i]
    if len(not_downloaded) > 0:
        # print("download new data")
        print(not_downloaded)
        download_pdf_from_data(not_downloaded)

    if any(exists):
        data = pd.concat((last_data, data)).drop_duplicates()
        save_data_pkl(data)
        return True
    return False


def download_pdf_from_data(data: pd.DataFrame, name="dates", url="url_pdf"):
    for _, row in data.iterrows():
        download_pdf(str(row[name]), row[url])


if __name__ == "__main__":
    # data = load_data_pkl()
    # a = data.sample(4)
    # save_data_pkl(a)
    new = verify_new_docs()
    print(new)
