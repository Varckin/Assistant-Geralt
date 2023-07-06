"""Use Python 3.11"""

import requests
from bs4 import BeautifulSoup


def translate_rus2tat(word: str = ""):
    url_rus_to_tat = "https://translate.tatar/translate?lang=0&text="
    response = requests.get(url_rus_to_tat + word)

    return response.content.decode("utf-8")


def translate_tat2rus(word: str = ""):
    url_tat_to_rus = "https://translate.tatar/translate?lang=1&text="
    response = requests.get(url_tat_to_rus + word)

    return response.content.decode("utf-8")


def prettify_result(result):
    data_parse = dict()
    soup = BeautifulSoup(result, 'html.parser')

    tmp = soup.select_one("responseType")
    data_parse["responseType"] = tmp.text if tmp else None

    tmp = soup.select_one("word")
    data_parse["word"] = tmp.text if tmp else None

    tmp = soup.select_one("pos")
    data_parse["pos"] = tmp.text if tmp else None

    tmp = soup.select("translation")
    tmp_list = []
    for val in tmp:
        tmp_list.append(val.text)
    data_parse["translation"] = tmp_list

    tmp = soup.select_one("examples")
    tmp_list = []
    for val in tmp:
        tmp_list.append(val.text)
    data_parse["examples"] = tmp_list

    tmp = soup.select_one("mt")
    data_parse["mt"] = tmp.text if tmp else None

    return data_parse

def decorated_result(result: dict):
    translate: str = ""
    for val in result["translation"]:
        translate += f"\n- {val}"

    example: str = ""
    for val in result["examples"]:
        example += f"\n- {val}"

    text = f"""
Word: {result["word"]}
Part of speech: {result["pos"]}
Translate: {translate}
Example: {example}
Word translate: {result["mt"]}
            """

    return text
