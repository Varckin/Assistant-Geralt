"""Use Python 3.11"""

import requests
from bs4 import BeautifulSoup

from main import bot, states, all_commands


def translate_rus2tat(word: str = ""):
    url_rus_to_tat = "https://translate.tatar/translate?lang=0&text="
    response = requests.get(url_rus_to_tat + word)

    return response.content.decode("utf-8")


def translate_tat2rus(word: str = ""):
    url_tat_to_rus = "https://translate.tatar/translate?lang=1&text="
    response = requests.get(url_tat_to_rus + word)

    return response.content.decode("utf-8")


def prettify_result(result: str):
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


@bot.message_handler(commands=['tat2rus'])
def tat2rus(message):
    chat_id = message.chat.id
    if chat_id in states and states[chat_id] == 'tat2rus':
        bot.send_message(message.chat.id, "The command are already being executed, write a word or proposal")
    else:
        states[chat_id] = 'tat2rus'
        bot.send_message(message.chat.id, "Enter word or proposal")


@bot.message_handler(commands=['rus2tat'])
def rus2tat(message):
    chat_id = message.chat.id
    if chat_id in states and states[chat_id] == 'rus2tat':
        bot.send_message(message.chat.id, "The command are already being executed, write a word or proposal")
    else:
        states[chat_id] = 'rus2tat'
        bot.send_message(message.chat.id, "Enter word or proposal")


@bot.message_handler(func=lambda message: (states.get(message.chat.id) in ['tat2rus', 'rus2tat']
                                           and message.text not in all_commands))
def else_message_tatrus(message):
    chat_id = message.chat.id
    if chat_id in states and states[chat_id] == 'rus2tat':
        try:
            text: str = message.text
            request: str = translate_rus2tat(text)
            if request.find("<res>") == 0:
                data: dict = prettify_result(request)
                bot.send_message(message.chat.id, decorated_result(data))
            else:
                bot.send_message(message.chat.id, request)
        except Exception as E:
            bot.send_message(message.chat.id, f"Error: {E}")
    elif chat_id in states and states[chat_id] == 'tat2rus':
        try:
            text: str = message.text
            request: str = translate_tat2rus(text)
            if request.find("<res>") == 0:
                data: dict = prettify_result(request)
                bot.send_message(message.chat.id, decorated_result(data))
            else:
                bot.send_message(message.chat.id, request)
        except Exception as E:
            bot.send_message(message.chat.id, f"Error: {E}")
