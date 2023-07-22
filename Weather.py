"""Use Python 3.11"""

import telebot
from json import loads
from urllib.parse import quote
from urllib.request import urlopen

from main import bot, all_commands, states

url: str = 'https://wttr.in/'
city_dic = {}


def current_weather(city: str):
    try:
        response = urlopen(f'{url}{quote(city)}?format=%l"+%m"+%t"+%w"+%C"+%T')
        data = response.read().decode()
        city_name, moon_phase, temperature, wind, weather_condition, request_time = data.split('"', 5)
        text: str = f'''
City name: {city_name}
Moon phase: {moon_phase}
Temperature: {temperature}
Wind: {wind}
Weather condition: {weather_condition}
Request time: {request_time}
'''
        return text
    except Exception:
        pass


def weather(city: str, num: int):
    try:
        response = urlopen(url+quote(city)+'?format=j1')
        data = loads(response.read().decode())
        w1, w2, w3 = data["weather"]
        cw = data["current_condition"][0]
        if num == 1:
            text: str = f'''
City name: {city}
Temperature °C: {cw["temp_C"]}
Temperature °F: {cw["temp_F"]}
Wind: {cw["windspeedKmph"]} km/h {cw["winddir16Point"]}
Weather condition: {cw["weatherDesc"][0]["value"]}
'''
            return text
        elif num == 2:
            text: str = f'''
City: {city}
Data: {w1["date"]}
Min and Max temp °C: {w1["mintempC"]}-{w1["maxtempC"]}
Min and Max temp °F: {w1["mintempF"]}-{w1["maxtempF"]}
Wind: {w1["hourly"][3]["windspeedKmph"]} km/h {w1["hourly"][3]["winddir16Point"]} 
Weather condition: {w1["hourly"][3]["weatherDesc"][0]["value"]}
Moon phase: {w1["astronomy"][0]["moon_phase"]}
'''
            return text
        elif num == 3:
            text: str = f'''
City: {city}
Data: {w2["date"]}
Min and Max temp °C: {w2["mintempC"]}-{w2["maxtempC"]}
Min and Max temp °F: {w2["mintempF"]}-{w2["maxtempF"]}
Wind: {w2["hourly"][3]["windspeedKmph"]} km/h {w2["hourly"][3]["winddir16Point"]} 
Weather condition: {w2["hourly"][3]["weatherDesc"][0]["value"]}
Moon phase: {w2["astronomy"][0]["moon_phase"]}
'''
            return text
        elif num == 4:
            text: str = f'''
City: {city}
Data: {w3["date"]}
Min and Max temp °C: {w3["mintempC"]}-{w3["maxtempC"]}
Min and Max temp °F: {w3["mintempF"]}-{w3["maxtempF"]}
Wind: {w3["hourly"][3]["windspeedKmph"]} km/h {w3["hourly"][3]["winddir16Point"]} 
Weather condition: {w3["hourly"][3]["weatherDesc"][0]["value"]}
Moon phase: {w3["astronomy"][0]["moon_phase"]}
'''
            return text
    except Exception:
        pass


def png(city: str):
    try:
        response = urlopen(url+quote(city)+'.png?p')
        data = response.read()

        return data
    except Exception:
        pass


markup_select_weather = telebot.types.InlineKeyboardMarkup()
markup_select_weather.row(
    telebot.types.InlineKeyboardButton('Current weather', callback_data='click_Current_weather'),
    telebot.types.InlineKeyboardButton('Today weather', callback_data='click_Today_weather'))
markup_select_weather.row(
    telebot.types.InlineKeyboardButton('Tomorrow weather', callback_data='click_Tomorrow_weather'),
    telebot.types.InlineKeyboardButton('The day after tomorrow weather', callback_data='click_tdatw'))
markup_select_weather.row(telebot.types.InlineKeyboardButton('Cancel', callback_data='click_cancel_weather'))


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


@bot.message_handler(func=lambda message: (states.get(message.chat.id) in ['weather', 'current_weather', 'weather_png']
                                           and message.text not in all_commands))
def else_message_weather(message):
    chat_id = message.chat.id
    if chat_id in states and states[chat_id] == 'current_weather':
        try:
            bot.send_message(message.chat.id, current_weather(message.text))
        except Exception as E:
            bot.send_message(message.chat.id, f"Error: {E}")
    elif chat_id in states and states[chat_id] == 'weather':
        city_dic[chat_id] = message.text
        bot.send_message(message.chat.id, "Select something from the suggested buttons.",
                         reply_markup=markup_select_weather)
    elif chat_id in states and states[chat_id] == 'weather_png':
        try:
            bot.send_photo(message.chat.id, png(message.text))
        except Exception as E:
            bot.send_message(message.chat.id, f"Error: {E}")


@bot.callback_query_handler(func=lambda call: (states.get(call.message.chat.id)
                                               in ['weather', 'current_weather', 'weather_png']))
def callback_handler(call):
    chat_id = call.message.chat.id
    try:
        if call.data == 'click_Current_weather':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=weather(city_dic[chat_id], 1), reply_markup=markup_select_weather)
        elif call.data == 'click_Today_weather':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=weather(city_dic[chat_id], 2), reply_markup=markup_select_weather)
        elif call.data == 'click_Tomorrow_weather':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=weather(city_dic[chat_id], 3), reply_markup=markup_select_weather)
        elif call.data == 'click_tdatw':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=weather(city_dic[chat_id], 4), reply_markup=markup_select_weather)
        elif call.data == 'click_cancel_weather':
            if chat_id in city_dic:
                del city_dic[chat_id]
            if chat_id in states:
                del states[chat_id]
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Cancel")
    except Exception as E:
        bot.send_message(call.message.chat.id, f"Error {E}")
