"""Use Python 3.11"""

import telebot
import Api_key
import Translate_tatar as Tt
import Weather as Wthr

bot = telebot.TeleBot(Api_key.API_KEY)
states = {}
city: str = ''


# Main command /start, /help, /about
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, f"Hello {message.from_user.first_name}")


@bot.message_handler(commands=['help'])
def help_command(message):
    text: str = f'''
/weather - Displays the weather for 3 days.
/png - creates a weather image for 3 days.
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
                                      "Version: 1.3\n Build: 136", parse_mode="Markdown")


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
        bot.send_message(message.chat.id, "The command are already being executed, write a word or sentence")
    else:
        states[chat_id] = 'tat2rus'
        bot.send_message(message.chat.id, "Enter word or proposal")


@bot.message_handler(commands=['rus2tat'])
def rus2tat(message):
    chat_id = message.chat.id
    if chat_id in states and states[chat_id] == 'rus2tat':
        bot.send_message(message.chat.id, "The command are already being executed, write a word or sentence")
    else:
        states[chat_id] = 'rus2tat'
        bot.send_message(message.chat.id, "Enter word or proposal")


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
        global city
        city = ''
        del states[chat_id]
        bot.send_message(message.chat.id, "Cancel operation", reply_markup=telebot.types.ReplyKeyboardRemove())
    elif chat_id in states and states[chat_id] == 'weather_png':
        del states[chat_id]
        bot.send_message(message.chat.id, "Cancel operation")
    else:
        bot.send_message(message.chat.id, "There are no actions to cancel.")


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
        global city
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        but1 = telebot.types.KeyboardButton("Current weather")
        but2 = telebot.types.KeyboardButton("Today weather")
        but3 = telebot.types.KeyboardButton("Tomorrow weather")
        but4 = telebot.types.KeyboardButton("The day after tomorrow weather")
        but5 = telebot.types.KeyboardButton("Cancel")
        keyboard.add(but1, but2, but3, but4, but5)

        if city == '':
            city = message.text
            bot.send_message(message.chat.id, "Select something from the suggested buttons.", reply_markup=keyboard)
        try:
            if message.text == "Current weather":
                bot.send_message(message.chat.id, Wthr.weather(city, 1))
            elif message.text == "Today weather":
                bot.send_message(message.chat.id, Wthr.weather(city, 2))
            elif message.text == "Tomorrow weather":
                bot.send_message(message.chat.id, Wthr.weather(city, 3))
            elif message.text == "The day after tomorrow weather":
                bot.send_message(message.chat.id, Wthr.weather(city, 4))
            elif message.text == "Cancel":
                city = ''
                del states[chat_id]
                bot.send_message(message.chat.id, "Cancel",
                                 reply_markup=telebot.types.ReplyKeyboardRemove())
        except Exception as E:
            bot.send_message(message.chat.id, f"Error: {E}")
    elif chat_id in states and states[chat_id] == 'weather_png':
        try:
            bot.send_photo(message.chat.id, Wthr.png(message.text))
        except Exception as E:
            bot.send_message(message.chat.id, f"Error: {E}")
    else:
        bot.send_message(message.chat.id, "Unknown command")


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Bot execution error: {e}")
