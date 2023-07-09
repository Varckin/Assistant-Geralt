"""Use Python 3.11"""

import requests

url = "https://api.mymemory.translated.net/"
language = {
    'Espanish-English': 'es|en',
    'Espanish-Russian': 'es|ru',
    'English-Russian': 'en|ru',
    'English-Espanish': 'en|es',
    'Russian-English': 'ru|en',
    'Russian-Espanish': 'ru|es'
}


def translate(lang: str, text: str):
    trnslt = f"get?q={text}&langpair={lang}&de=varckin@protonmail.com"
    response = requests.get(url + trnslt)
    json_data = response.json()

    return json_data['responseData']['translatedText']
