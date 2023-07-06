"""Use Python 3.11"""

import telebot
import Api_key
import Translate_tatar as Tt

bot = telebot.TeleBot(Api_key.API_KEY)
states = {}


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, f"Hello {message.from_user.first_name}")


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


@bot.message_handler(commands=['cancel'])
def cancel(message):
    chat_id = message.chat.id
    if chat_id in states and states[chat_id] == 'rus2tat':
        del states[chat_id]
        bot.send_message(message.chat.id, "Cancel operation")
    elif chat_id in states and states[chat_id] == 'tat2rus':
        del states[chat_id]
        bot.send_message(message.chat.id, "Cancel operation")
    else:
        bot.send_message(message.chat.id, "There are no actions to cancel.")


@bot.message_handler(commands=['M'])
def cancel(message):
    bot.send_message(message.chat.id, str(states))


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
        except Exception:
            bot.send_message(message.chat.id, "You entered the wrong value. Enter the /cancel command again")
    elif chat_id in states and states[chat_id] == 'tat2rus':
        try:
            text: str = message.text
            request: str = Tt.translate_tat2rus(text)
            if request.find("<res>") == 0:
                data: dict = Tt.prettify_result(request)
                bot.send_message(message.chat.id, Tt.decorated_result(data))
            else:
                bot.send_message(message.chat.id, request)
        except Exception:
            bot.send_message(message.chat.id, "You entered the wrong value. Enter the /cancel command again")
    else:
        bot.send_message(message.chat.id, "Unknown command")


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Bot execution error: {e}")
