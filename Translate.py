"""Use Python 3.11"""

import requests
import telebot

from main import bot, states, all_commands

lang_dic = {}
url = "https://api.mymemory.translated.net/"
language = {
    'Espanish-English': 'es|en',
    'Espanish-Russian': 'es|ru',
    'English-Russian': 'en|ru',
    'English-Espanish': 'en|es',
    'Russian-English': 'ru|en',
    'Russian-Espanish': 'ru|es'
}

markup_change_translate = telebot.types.InlineKeyboardMarkup()
markup_change_translate.row(
    telebot.types.InlineKeyboardButton('Espanish-English', callback_data='click_Espanish_English'),
    telebot.types.InlineKeyboardButton('Espanish-Russian', callback_data='click_Espanish_Russian'))
markup_change_translate.row(
    telebot.types.InlineKeyboardButton('English-Russian', callback_data='click_English_Russian'),
    telebot.types.InlineKeyboardButton('English-Espanish', callback_data='click_English_Espanish'))
markup_change_translate.row(
    telebot.types.InlineKeyboardButton('Russian-English', callback_data='click_Russian_English'),
    telebot.types.InlineKeyboardButton('Russian-Espanish', callback_data='click_Russian_Espanish'))
markup_change_translate.row(telebot.types.InlineKeyboardButton('Cancel', callback_data='click_cancel_translate'))


def translate(lang: str, text: str):
    trnslt = f"get?q={text}&langpair={lang}&de=varckin@protonmail.com"
    response = requests.get(url + trnslt)
    json_data = response.json()

    return json_data['responseData']['translatedText']


@bot.message_handler(commands=['translate'])
def translate_command(message):
    chat_id = message.chat.id
    if chat_id in states and states[chat_id] == 'translate':
        bot.send_message(message.chat.id, "The command are already being executed, write a word or proposal")
    else:
        states[chat_id] = 'translate'
        bot.send_message(message.chat.id, "Select languages", reply_markup=markup_change_translate)


@bot.message_handler(commands=['change_language'])
def change_language(message):
    chat_id = message.chat.id
    if chat_id in states and states[chat_id] == 'translate':
        bot.send_message(message.chat.id, "Select languages", reply_markup=markup_change_translate)
    else:
        bot.send_message(message.chat.id, "You are not translating the text. enter /translate to translate the text.")


@bot.message_handler(func=lambda message: (states.get(message.chat.id) in ['translate']
                                           and message.text not in all_commands))
def else_message_translate(message):
    chat_id = message.chat.id
    if chat_id in states and states[chat_id] == 'translate':
        try:
            if lang_dic[chat_id] == "Espanish-English":
                bot.send_message(message.chat.id, translate(language[lang_dic[chat_id]], message.text))
            elif lang_dic[chat_id] == "Espanish-Russian":
                bot.send_message(message.chat.id, translate(language[lang_dic[chat_id]], message.text))
            elif lang_dic[chat_id] == "English-Russian":
                bot.send_message(message.chat.id, translate(language[lang_dic[chat_id]], message.text))
            elif lang_dic[chat_id] == "English-Espanish":
                bot.send_message(message.chat.id, translate(language[lang_dic[chat_id]], message.text))
            elif lang_dic[chat_id] == "Russian-English":
                bot.send_message(message.chat.id, translate(language[lang_dic[chat_id]], message.text))
            elif lang_dic[chat_id] == "Russian-Espanish":
                bot.send_message(message.chat.id, translate(language[lang_dic[chat_id]], message.text))
        except Exception as E:
            bot.send_message(message.chat.id, f"Error: {E}")


@bot.callback_query_handler(func=lambda call: states.get(call.message.chat.id) in ['translate'])
def callback_handler(call):
    chat_id = call.message.chat.id
    try:
        if call.data == 'click_Espanish_English':
            lang_dic[chat_id] = 'Espanish-English'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Selected language. Enter text")
        elif call.data == 'click_Espanish_Russian':
            lang_dic[chat_id] = 'Espanish-Russian'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Selected language. Enter text")
        elif call.data == 'click_English_Russian':
            lang_dic[chat_id] = 'English-Russian'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Selected language. Enter text")
        elif call.data == 'click_English_Espanish':
            lang_dic[chat_id] = 'English-Espanish'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Selected language. Enter text")
        elif call.data == 'click_Russian_English':
            lang_dic[chat_id] = 'Russian-English'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Selected language. Enter text")
        elif call.data == 'click_Russian_Espanish':
            lang_dic[chat_id] = 'Russian-Espanish'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Selected language. Enter text")
        elif call.data == 'click_cancel_translate':
            if chat_id in lang_dic:
                del lang_dic[chat_id]
            if chat_id in states:
                del states[chat_id]
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Cancel")
    except Exception as E:
        bot.send_message(call.message.chat.id, f"Error {E}")
