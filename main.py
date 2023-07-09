"""Use Python 3.11"""

import telebot
import Api_key
import Translate_tatar as Tt
import Weather as Wthr
import Translate as Trnslt

bot = telebot.TeleBot(Api_key.API_KEY)
states = {}
city = {}
lang = {}


# Keyboard to weather and change translate
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


# Main command /start, /help, /about
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, f"Hello {message.from_user.first_name}")


@bot.message_handler(commands=['help'])
def help_command(message):
    text: str = f'''
/weather - Displays the weather for 3 days.
/weather_png - creates a weather image for 3 days.
/current_weather - shows the current weather.
/tat2rus - translate tatar to russian.
/rus2tat - translate russian to tatar.
/help - displays information about commands.
/about - displays information about the bot.
/cancel - Cancel all commands
'''
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['about'])
def about_command(message):
    bot.send_message(message.chat.id, "Creator: [Markus Varckin](t.me/Varckin)\n"
                                      "Version: 1.3\nBuild: 136", parse_mode="Markdown")


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
    else:
        bot.send_message(message.chat.id, "There are no actions to cancel.")


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global lang, city
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
        elif call.data == 'click_cancel':
            if chat_id in lang:
                del lang[chat_id]
            elif chat_id in city:
                del city[chat_id]
            elif chat_id in states:
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
    else:
        bot.send_message(message.chat.id, "Unknown command")


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Bot execution error: {e}")
