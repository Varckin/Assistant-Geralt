"""Use Python 3.11"""

import sqlite3
import datetime

from main import bot
import Data_base as Db


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
/generator - generator passcode.
/gallows - game gallows.
/anonim_mail - random anonim email.
/help - displays information about commands.
/about - displays information about the bot.
/cancel - Cancel all commands
'''
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['about'])
def about_command(message):
    bot.send_message(message.chat.id, "Creator: [Markus Varckin](t.me/Varckin)\n"
                                      "Version: 2.17\nBuild: 203", parse_mode="Markdown")
