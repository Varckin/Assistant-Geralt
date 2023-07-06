"""Use Python 3.11"""

import telebot
import Api_key
import Translate_tatar as Tt

bot = telebot.TeleBot(Api_key.API_KEY)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, f"Hello {message.from_user.first_name}")


@bot.message_handler(commands=['tat2rus'])
def tat2rus(message):
    text = message.text.split(' ', 1)
    try:
        if len(text) == 2:
            request: str = Tt.translate_tat2rus(str(text[1]))
            if request.find("<res>") == 0:
                data: dict = Tt.prettify_result(request)
                bot.send_message(message.chat.id, Tt.decorated_result(data))
            else:
                bot.send_message(message.chat.id, request)
        else:
            bot.send_message(message.chat.id, "Enter word or proposal")
            bot.register_next_step_handler(message, tat2rus_2)
    except Exception:
        bot.send_message(message.chat.id, "You entered the wrong value. Enter the /tat2rus command again")


def tat2rus_2(message):
    request: str = Tt.translate_tat2rus(str(message.text))
    if request.find("<res>") == 0:
        data: dict = Tt.prettify_result(request)
        bot.send_message(message.chat.id, Tt.decorated_result(data))
    else:
        bot.send_message(message.chat.id, request)


@bot.message_handler(commands=['rus2tat'])
def rus2tat(message):
    text = message.text.split(' ', 1)
    try:
        if len(text) == 2:
            request: str = Tt.translate_rus2tat(str(text[1]))
            if request.find("<res>") == 0:
                data: dict = Tt.prettify_result(request)
                bot.send_message(message.chat.id, Tt.decorated_result(data))
            else:
                bot.send_message(message.chat.id, request)
        else:
            bot.send_message(message.chat.id, "Enter word or proposal")
            bot.register_next_step_handler(message, rus2tat_2)
    except Exception:
        bot.send_message(message.chat.id, "You entered the wrong value. Enter the /tat2rus command again")


def rus2tat_2(message):
    request: str = Tt.translate_rus2tat(str(message.text))
    if request.find("<res>") == 0:
        data: dict = Tt.prettify_result(request)
        bot.send_message(message.chat.id, Tt.decorated_result(data))
    else:
        bot.send_message(message.chat.id, request)


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Bot execution error: {e}")
