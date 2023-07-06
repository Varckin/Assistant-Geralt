from json import loads
from urllib.parse import quote
from urllib.request import urlopen

url = 'https://wttr.in/'


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
    except Exception as e:
        print(e)


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
    except Exception as e:
        print(e)


def png(city: str):
    try:
        response = urlopen(url+quote(city)+'.png?p')
        data = response.read()

        return data
    except Exception as e:
        print(e)
