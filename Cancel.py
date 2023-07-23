from main import bot, states
from Weather import city_dic
from Translate import lang_dic
from Gallows import tries, word, guessed_word, guessed_letters, guess
from Generator import length_password
from Anonim_Mail import email


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
        if chat_id in city_dic:
            del city_dic[chat_id]
        del states[chat_id]
        bot.send_message(message.chat.id, "Cancel operation")
    elif chat_id in states and states[chat_id] == 'weather_png':
        del states[chat_id]
        bot.send_message(message.chat.id, "Cancel operation")
    elif chat_id in states and states[chat_id] == 'translate':
        if chat_id in lang_dic:
            del lang_dic[chat_id]
        del states[chat_id]
        bot.send_message(message.chat.id, "Cancel operation")
    elif chat_id in states and states[chat_id] == 'generator_password':
        del states[chat_id]
        del length_password[chat_id]
        bot.send_message(message.chat.id, "Cancel operation")
    elif chat_id in states and states[chat_id] == 'gallows':
        del tries[chat_id]
        del word[chat_id]
        del guessed_word[chat_id]
        del guessed_letters[chat_id]
        del guess[chat_id]
        del states[chat_id]
        bot.send_message(message.chat.id, "Cancel operation")
    elif chat_id in states and states[chat_id] == 'anonim_mail':
        del email[chat_id]
        del states[chat_id]
        bot.send_message(message.chat.id, "Cancel operation")
    else:
        bot.send_message(message.chat.id, "There are no actions to cancel.")


@bot.message_handler(func=lambda message: True)
def else_messages(message):
    bot.send_message(message.chat.id, "Unknown command")
