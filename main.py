"""Use Python 3.11"""

import telebot
import sqlite3
import datetime
import random
import Api_key
import Translate_tatar as Tt
import Weather as Wthr
import Translate as Trnslt
import Data_base as Db
import Gallows as Gs


bot = telebot.TeleBot(Api_key.API_KEY)
states = {}
city = {}
lang = {}
length = {}

tries = {}
word = {}
guessed_word = {}
guessed_letters = {}
guess = {}


# Keyboard to weather, change translate and generator
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
markup_change_translate.row(telebot.types.InlineKeyboardButton('Cancel', callback_data='click_cancel'))


markup_select_weather = telebot.types.InlineKeyboardMarkup()
markup_select_weather.row(
    telebot.types.InlineKeyboardButton('Current weather', callback_data='click_Current_weather'),
    telebot.types.InlineKeyboardButton('Today weather', callback_data='click_Today_weather'))
markup_select_weather.row(
    telebot.types.InlineKeyboardButton('Tomorrow weather', callback_data='click_Tomorrow_weather'),
    telebot.types.InlineKeyboardButton('The day after tomorrow weather', callback_data='click_tdatw'))
markup_select_weather.row(telebot.types.InlineKeyboardButton('Cancel', callback_data='click_cancel'))


markup_generator = telebot.types.InlineKeyboardMarkup()
markup_generator.row(telebot.types.InlineKeyboardButton('Refresh', callback_data='click_Generator'))


# Main command /start, /help, /about, /generator
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, f"Hello {message.from_user.first_name}")
    db = sqlite3.connect(Db.name_base)
    cursor = db.cursor()
    id_user: int = message.from_user.id
    name_user: str = message.from_user.first_name
    date: str = datetime.date.today().strftime('%d-%m-%Y')
    if cursor.execute("SELECT COUNT(id_user) FROM users WHERE id_user=?", (id_user,)).fetchone()[0] == 0:
        cursor.execute(" INSERT INTO users (id_user, name, date_registration) VALUES (?, ?, ?)",
                       (id_user, name_user, date))
        db.commit()
        db.close()


@bot.message_handler(commands=['help'])
def help_command(message):
    text: str = f'''
/weather - Displays the weather for 3 days.
/weather_png - creates a weather image for 3 days.
/current_weather - shows the current weather.
/tat2rus - translate tatar to russian.
/rus2tat - translate russian to tatar.
/translate - translate word or or proposal.
/change_language - change language translate.
/generator - generator passcode
/help - displays information about commands.
/about - displays information about the bot.
/cancel - Cancel all commands
'''
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['about'])
def about_command(message):
    bot.send_message(message.chat.id, "Creator: [Markus Varckin](t.me/Varckin)\n"
                                      "Version: 2.12\nBuild: 189", parse_mode="Markdown")


@bot.message_handler(commands=['generator'])
def generator_command(message):
    chat_id = message.chat.id
    if chat_id in states and states[chat_id] == 'generator':
        bot.send_message(message.chat.id, "The command are already being executed, write length password")
    else:
        states[chat_id] = 'generator'
        bot.send_message(message.chat.id, "Enter length password")


# Command /weather, /current_weather, /weather_png
@bot.message_handler(commands=['current_weather'])
def current_weather_command(message):
    chat_id = message.chat.id
    if chat_id in states and states[chat_id] == 'current_weather':
        bot.send_message(message.chat.id, "The command are already being executed, write city")
    else:
        states[chat_id] = 'current_weather'
        bot.send_message(message.chat.id, "Enter city")


@bot.message_handler(commands=['weather'])
def weather_command(message):
    chat_id = message.chat.id
    if chat_id in states and states[chat_id] == 'weather':
        bot.send_message(message.chat.id, "The command are already being executed, write city")
    else:
        states[chat_id] = 'weather'
        bot.send_message(message.chat.id, "Enter city")


@bot.message_handler(commands=['weather_png'])
def weather_png_command(message):
    chat_id = message.chat.id
    if chat_id in states and states[chat_id] == 'weather_png':
        bot.send_message(message.chat.id, "The command are already being executed, write city")
    else:
        states[chat_id] = 'weather_png'
        bot.send_message(message.chat.id, "Enter city")


# Command translate tatar and russian
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


# command translate other language
@bot.message_handler(commands=['translate'])
def translate(message):
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


@bot.message_handler(commands=['gallows'])
def gallows_command(message):
    chat_id = message.chat.id
    if chat_id in states and states[chat_id] == 'gallows':
        bot.send_message(message.chat.id, "The command are already being executed")
    else:
        states[chat_id] = 'gallows'
        tries[chat_id] = 8
        word[chat_id] = random.choice(Gs.words).lower()
        guessed_word[chat_id] = ''
        guessed_letters[chat_id] = []

        for letter in word[chat_id]:
            if letter in guessed_letters[chat_id]:
                guessed_word[chat_id] += letter
            else:
                guessed_word[chat_id] += '_'

        bot.send_message(message.chat.id, f"The word is selected. Write the letter.\n"
                                          f"Guessed word: {guessed_word[chat_id]}\n"
                                          f"Tries: {tries[chat_id]}")


# Cancel command
@bot.message_handler(commands=['cancel'])
def cancel(message):
    chat_id = message.chat.id
    if chat_id in states and states[chat_id] == 'rus2tat':
        del states[chat_id]
        bot.send_message(message.chat.id, "Cancel operation")
    elif chat_id in states and states[chat_id] == 'tat2rus':
        del states[chat_id]
        bot.send_message(message.chat.id, "Cancel operation")
    elif chat_id in states and states[chat_id] == 'current_weather':
        del states[chat_id]
        bot.send_message(message.chat.id, "Cancel operation")
    elif chat_id in states and states[chat_id] == 'weather':
        if chat_id in city:
            del city[chat_id]
        del states[chat_id]
        bot.send_message(message.chat.id, "Cancel operation")
    elif chat_id in states and states[chat_id] == 'weather_png':
        del states[chat_id]
        bot.send_message(message.chat.id, "Cancel operation")
    elif chat_id in states and states[chat_id] == 'translate':
        if chat_id in lang:
            del lang[chat_id]
        del states[chat_id]
        bot.send_message(message.chat.id, "Cancel operation")
    elif chat_id in states and states[chat_id] == 'generator':
        del states[chat_id]
        del length[chat_id]
        bot.send_message(message.chat.id, "Cancel operation")
    elif chat_id in states and states[chat_id] == 'gallows':
        del tries[chat_id]
        del word[chat_id]
        del guessed_word[chat_id]
        del guessed_letters[chat_id]
        del guess[chat_id]
        del states[chat_id]
        bot.send_message(message.chat.id, "Cancel operation")
    else:
        bot.send_message(message.chat.id, "There are no actions to cancel.")


# callback to markup
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global lang, city, length
    chat_id = call.message.chat.id
    try:
        if call.data == 'click_Espanish_English':
            lang[chat_id] = 'Espanish-English'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Selected language. Enter text")
        elif call.data == 'click_Espanish_Russian':
            lang[chat_id] = 'Espanish-Russian'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Selected language. Enter text")
        elif call.data == 'click_English_Russian':
            lang[chat_id] = 'English-Russian'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Selected language. Enter text")
        elif call.data == 'click_English_Espanish':
            lang[chat_id] = 'English-Espanish'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Selected language. Enter text")
        elif call.data == 'click_Russian_English':
            lang[chat_id] = 'Russian-English'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Selected language. Enter text")
        elif call.data == 'click_Russian_Espanish':
            lang[chat_id] = 'Russian-Espanish'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Selected language. Enter text")
        elif call.data == 'click_Current_weather':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=Wthr.weather(city[chat_id], 1), reply_markup=markup_select_weather)
        elif call.data == 'click_Today_weather':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=Wthr.weather(city[chat_id], 2), reply_markup=markup_select_weather)
        elif call.data == 'click_Tomorrow_weather':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=Wthr.weather(city[chat_id], 3), reply_markup=markup_select_weather)
        elif call.data == 'click_tdatw':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=Wthr.weather(city[chat_id], 4), reply_markup=markup_select_weather)
        elif call.data == 'click_Generator':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=Db.generate_password(length[chat_id]), reply_markup=markup_generator)
        elif call.data == 'click_cancel':
            if chat_id in lang:
                del lang[chat_id]
            if chat_id in city:
                del city[chat_id]
            if chat_id in states:
                del states[chat_id]
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Cancel")
    except Exception as E:
        bot.send_message(call.message.chat.id, f"Error {E}")


# State processing. "ELSE" - Processes all other messages
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    if chat_id in states and states[chat_id] == 'rus2tat':
        try:
            text: str = message.text
            request: str = Tt.translate_rus2tat(text)
            if request.find("<res>") == 0:
                data: dict = Tt.prettify_result(request)
                bot.send_message(message.chat.id, Tt.decorated_result(data))
            else:
                bot.send_message(message.chat.id, request)
        except Exception as E:
            bot.send_message(message.chat.id, f"Error: {E}")
    elif chat_id in states and states[chat_id] == 'tat2rus':
        try:
            text: str = message.text
            request: str = Tt.translate_tat2rus(text)
            if request.find("<res>") == 0:
                data: dict = Tt.prettify_result(request)
                bot.send_message(message.chat.id, Tt.decorated_result(data))
            else:
                bot.send_message(message.chat.id, request)
        except Exception as E:
            bot.send_message(message.chat.id, f"Error: {E}")
    elif chat_id in states and states[chat_id] == 'current_weather':
        try:
            bot.send_message(message.chat.id, Wthr.current_weather(message.text))
        except Exception as E:
            bot.send_message(message.chat.id, f"Error: {E}")
    elif chat_id in states and states[chat_id] == 'weather':
        city[chat_id] = message.text
        bot.send_message(message.chat.id, "Select something from the suggested buttons.",
                         reply_markup=markup_select_weather)
    elif chat_id in states and states[chat_id] == 'weather_png':
        try:
            bot.send_photo(message.chat.id, Wthr.png(message.text))
        except Exception as E:
            bot.send_message(message.chat.id, f"Error: {E}")
    elif chat_id in states and states[chat_id] == 'translate':
        try:
            if lang[chat_id] == "Espanish-English":
                bot.send_message(message.chat.id, Trnslt.translate(Trnslt.language[lang[chat_id]], message.text))
            elif lang[chat_id] == "Espanish-Russian":
                bot.send_message(message.chat.id, Trnslt.translate(Trnslt.language[lang[chat_id]], message.text))
            elif lang[chat_id] == "English-Russian":
                bot.send_message(message.chat.id, Trnslt.translate(Trnslt.language[lang[chat_id]], message.text))
            elif lang[chat_id] == "English-Espanish":
                bot.send_message(message.chat.id, Trnslt.translate(Trnslt.language[lang[chat_id]], message.text))
            elif lang[chat_id] == "Russian-English":
                bot.send_message(message.chat.id, Trnslt.translate(Trnslt.language[lang[chat_id]], message.text))
            elif lang[chat_id] == "Russian-Espanish":
                bot.send_message(message.chat.id, Trnslt.translate(Trnslt.language[lang[chat_id]], message.text))
        except Exception as E:
            bot.send_message(message.chat.id, f"Error: {E}")
    elif chat_id in states and states[chat_id] == 'generator':
        try:
            length[chat_id] = int(message.text)
            bot.send_message(message.chat.id, Db.generate_password(length[chat_id]), reply_markup=markup_generator)
        except Exception:
            bot.send_message(message.chat.id, 'Enter a number')
    elif chat_id in states and states[chat_id] == 'gallows':
        global tries, guessed_word, guessed_letters, guess, word

        guess[chat_id] = message.text.lower()
        if len(guess[chat_id]) != 1:
            bot.send_message(message.chat.id, f"Please enter only one letter.\n"
                                              f"Guessed word: {guessed_word[chat_id]}")
        elif guess[chat_id] in guessed_letters[chat_id]:
            bot.send_message(message.chat.id, f"You have already guessed this letter.\n"
                                              f"Guessed word: {guessed_word[chat_id]}")
        elif guess[chat_id] in word[chat_id]:
            guessed_word[chat_id] = ''
            guessed_letters[chat_id].append(guess[chat_id])

            for letter in word[chat_id]:
                if letter in guessed_letters[chat_id]:
                    guessed_word[chat_id] += letter
                else:
                    guessed_word[chat_id] += '_'
            print(guessed_word[chat_id])

            bot.send_message(message.chat.id, f"Right!\n"
                                              f"Guessed word: {guessed_word[chat_id]}")
        else:
            tries[chat_id] -= 1
            bot.send_message(message.chat.id, f"Wrong!\n"
                                              f"Guessed word: {guessed_word[chat_id]}\n"
                                              f"Tries: {tries[chat_id]}")
            guessed_letters[chat_id].append(guess[chat_id])

        if tries[chat_id] == 0:
            bot.send_message(message.chat.id, f"You've lost! The hidden word was: {word[chat_id]}")

        if guessed_word[chat_id] == word[chat_id]:
            bot.send_message(message.chat.id, "Congratulations! You've won!")
    else:
        bot.send_message(message.chat.id, "Unknown command")


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Bot execution error: {e}")
