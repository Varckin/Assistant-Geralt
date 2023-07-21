import telebot
import Api_key

bot = telebot.TeleBot(Api_key.API_KEY)

states = {}
all_commands = ['/start', '/weather', '/weather_png', '/current_weather', '/tat2rus', '/rus2tat', '/translate',
                '/change_language', '/generator', '/gallows', '/help', '/about', '/cancel']
