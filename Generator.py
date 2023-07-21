import telebot
import string
import random

from main import bot, states, all_commands

length_password = {}

markup_generator = telebot.types.InlineKeyboardMarkup()
markup_generator.row(telebot.types.InlineKeyboardButton('Refresh', callback_data='click_Generator_password'))


def generate_password(length: int):
    characters: str = string.ascii_letters + string.digits + string.punctuation
    password: str = ''.join(random.choice(characters) for _ in range(length))
    return password


@bot.message_handler(commands=['generator'])
def generator_command(message):
    chat_id = message.chat.id
    if chat_id in states and states[chat_id] == 'generator_password':
        bot.send_message(message.chat.id, "The command are already being executed, write length password")
    else:
        states[chat_id] = 'generator_password'
        bot.send_message(message.chat.id, "Enter length password")


@bot.message_handler(func=lambda message: (states.get(message.chat.id) in ['generator_password']
                                           and message.text not in all_commands))
def else_message_generator(message):
    chat_id = message.chat.id
    if chat_id in states and states[chat_id] == 'generator_password':
        try:
            length_password[chat_id] = int(message.text)
            bot.send_message(message.chat.id, generate_password(length_password[chat_id]),
                             reply_markup=markup_generator)
        except Exception:
            bot.send_message(message.chat.id, 'Enter a number')


@bot.callback_query_handler(func=lambda call: states.get(call.message.chat.id) in ['generator_password'])
def callback_handler(call):
    chat_id = call.message.chat.id
    try:
        if call.data == 'click_Generator_password':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=generate_password(int(length_password[chat_id])), reply_markup=markup_generator)
    except Exception as E:
        bot.send_message(call.message.chat.id, f"Error {E}")
