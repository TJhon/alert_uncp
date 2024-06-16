import requests, os, pickle, re

MAIN_DIR_PDF = "./pdfs"
last_data_path = "./data/last_data.pkl"


def download_pdf(name_file, url, main_dir=MAIN_DIR_PDF):
    pdf_url = requests.get(url)
    name_file = str(name_file).replace("-", "_").replace(" ", ":").split(":")[0]
    path_file = f"{main_dir}/{name_file}.pdf"
    # print(path_file)
    if not os.path.exists(path_file):
        with open(path_file, "wb") as f:
            f.write(pdf_url.content)
    return path_file


def save_data_pkl(data):
    with open(last_data_path, "wb") as f:
        pickle.dump(data, f)


def load_data_pkl(path=last_data_path):
    with open(path, "rb") as f:
        last_data = pickle.load(f)
    return last_data


def replace_special_characters(text):
    """
    Reemplaza los caracteres especiales en un texto por versiones equivalentes compatibles con ASCII o UTF-8.

    Parámetros:
    - text: Cadena de texto a procesar.

    Retorna:
    - Cadena de texto con caracteres especiales reemplazados.
    """
    # Definir un diccionario de reemplazo para caracteres especiales comunes
    replace_dict = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",  # Vocales acentuadas
        "Á": "A",
        "É": "E",
        "Í": "I",
        "Ó": "O",
        "Ú": "U",  # Vocales mayúsculas acentuadas
        "ñ": "n",
        "Ñ": "N",  # Letras ñ y Ñ
        "ü": "u",
        "Ü": "U",  # Letras ü y Ü
        "¿": "",
        "¡": "",  # Signos de interrogación y exclamación invertidos
        "º": "o",
        "ª": "a",  # Ordinales
        "«": '"',
        "»": '"',  # Comillas angulares francesas
        "€": "euros",
        "₧": "pesetas",  # Signos monetarios
        "ä": "a",
        "ë": "e",
        "ï": "i",
        "ö": "o",
        "ü": "u",  # Vocales con diéresis
        "Ä": "A",
        "Ë": "E",
        "Ï": "I",
        "Ö": "O",
        "Ü": "U",  # Vocales mayúsculas con diéresis
    }

    # Utilizar expresiones regulares para reemplazar caracteres especiales
    pattern = re.compile("|".join(replace_dict.keys()))
    processed_text = pattern.sub(lambda m: replace_dict[m.group()], text)

    return processed_text
