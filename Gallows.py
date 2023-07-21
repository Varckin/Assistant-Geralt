"""Use Python 3.11"""

import random

from main import bot, states, all_commands

tries = {}
word = {}
guessed_word = {}
guessed_letters = {}
guess = {}
words = []

with open('resourse/words.txt', 'r', encoding='utf-8') as file:
    words = file.read().split()


@bot.message_handler(commands=['gallows'])
def gallows_command(message):
    chat_id = message.chat.id
    if chat_id in states and states[chat_id] == 'gallows':
        bot.send_message(message.chat.id, "The command are already being executed")
    else:
        states[chat_id] = 'gallows'
        tries[chat_id] = 8
        word[chat_id] = random.choice(words).lower()
        guessed_word[chat_id] = ''
        guessed_letters[chat_id] = []

        for letter in word[chat_id]:
            if letter in guessed_letters[chat_id]:
                guessed_word[chat_id] += letter
            else:
                guessed_word[chat_id] += '*'

        bot.send_message(message.chat.id, f"The word is selected. Write the letter.\n"
                                          f"Guessed word: {guessed_word[chat_id]}\n"
                                          f"Tries: {tries[chat_id]}")


@bot.message_handler(func=lambda message: (states.get(message.chat.id) in ['gallows']
                                           and message.text not in all_commands))
def else_message_gallows(message):
    chat_id = message.chat.id
    if chat_id in states and states[chat_id] == 'gallows':
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
                    guessed_word[chat_id] += '*'

            if guessed_word[chat_id] == word[chat_id]:
                bot.send_message(message.chat.id, f"Congratulations! You've won!\n"
                                                  f"Guessed word: {guessed_word[chat_id]}")
                del tries[chat_id]
                del word[chat_id]
                del guessed_word[chat_id]
                del guessed_letters[chat_id]
                del guess[chat_id]
                del states[chat_id]
            else:
                bot.send_message(message.chat.id, f"Right!\n"
                                                  f"Guessed word: {guessed_word[chat_id]}")
        else:
            tries[chat_id] -= 1
            if tries[chat_id] == 0:
                bot.send_message(message.chat.id, f"You've lost! The hidden word was: {word[chat_id]}")
                with open('resourse/gallows_lose.gif', 'rb') as gif_file:
                    bot.send_animation(message.chat.id, gif_file)
                del tries[chat_id]
                del word[chat_id]
                del guessed_word[chat_id]
                del guessed_letters[chat_id]
                del guess[chat_id]
                del states[chat_id]
            else:
                bot.send_message(message.chat.id, f"Wrong!\n"
                                                  f"Guessed word: {guessed_word[chat_id]}\n"
                                                  f"Tries: {tries[chat_id]}")
                guessed_letters[chat_id].append(guess[chat_id])
