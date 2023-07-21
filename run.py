from main import bot
import Base_commands
import Translate_tatar
import Weather
import Translate
import Generator
import Gallows
import Cancel


if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Bot execution error: {e}")
