from pypdf import PdfReader as pdf
import re, os, pandas as pd
from datetime import datetime

now = datetime.now().strftime("%Y-%m-%d")

from utils import MAIN_DIR_PDF, load_data_pkl
from send_mail import pretty_content, send_email
from sele_request import verify_new_docs

targets = ["flores ro", "jhon kevin"]

verify_new_docs()
data = load_data_pkl()
names_pdf = data["name_pdf"]
pdf_url = data["url_pdf"]
pdfs_path = [f"{MAIN_DIR_PDF}/{name}.pdf" for name in names_pdf]


def search_user_pdf(pdf_path, targets, url_pdf):
    reader = pdf(pdf_path)
    pages = reader.pages
    last_relation = ""
    last_fac = ""
    # found_in = {}
    content = []
    url = []
    relations, pages_nu, facs, pdfs = [], [], [], []
    for page in pages:
        text = page.extract_text()
        lines = text.split("\n")
        for line_num, line in enumerate(lines):
            line = re.sub(r"\s+", " ", line)
            for target in targets:
                if "relación".lower() in line.lower():
                    last_relation = line
                if "facultad".lower() in line.lower():
                    last_fac = line
                if target.lower() in line.lower():
                    pdfs.append(pdf_path)
                    url.append(url_pdf)
                    pages_nu.append(page.page_number + 1)
                    relations.append(last_relation)
                    facs.append(last_fac)
                    content.append(line)

    return pd.DataFrame(
        {
            "Content": content,
            "PDF": url,
            "Page": pages_nu,
            "Relation": relations,
            "Faculty": facs,
        }
    ).drop_duplicates()


found_text = pd.DataFrame()

for pdf_path, url in zip(pdfs_path, pdf_url):
    # print(pdf_path)
    found = search_user_pdf(pdf_path, targets, url)
    if len(found) > 0:
        found_text = pd.concat((found_text, found))

content = "Contenido encontrado\n"


if len(found_text) > 0:
    for index, row in found_text.iterrows():
        content_i = pretty_content(
            row["Content"],
            row["PDF"],
            row["Page"],
            row["Relation"],
            row["Faculty"],
        )
        content += content_i
    send_email(content, f"Busqueda de UNCP - {now}")