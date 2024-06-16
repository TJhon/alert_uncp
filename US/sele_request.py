from selenium import webdriver
import time, pandas as pd, numpy as np
from selenium.webdriver.common.by import By

import pickle
from utils import download_pdf, save_data_pkl, load_data_pkl

MAIN_URL = "https://resoluciones.uncp.edu.pe/documentos/R-EC"
last_data_path = "./data/last_data.pkl"


def get_actual_data():

    driver = webdriver.Chrome()
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
    print(not_downloaded)
    if len(not_downloaded) > 0:
        # print("download new data")
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
    # get_actual_data().to_parquet("./data/actual.parquet")
    # data = load_data_pkl()
    save_data_pkl(pd.DataFrame({"dates": []}))
    # print("dummy_data")
    # d_data = get_actual_data().sample(9)
    # print(d_data)
    # download_pdf_from_data(d_data)
    # print("verify data")
    new = verify_new_docs()
    print(new)
