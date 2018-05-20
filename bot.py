from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    """Send a message when the command /start is issued."""
    bot.send_message(chat_id=update.message.chat_id,
                     text="I'm a telegram-bot that "
                          "shows you the weather in any city!")
    bot.send_message(chat_id=update.message.chat_id,
                     text="You can use some commands: \n"
                          "/caps <arguments> \n"
                          "/weather <city>")


def echo(bot, update):
    """Echo the user message."""
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)


def Weather(bot, update, args):
    city = args
    appid = "ad90afdfa34918d01559579762da4f03"
    result = requests.get("http://api.openweathermap.org/data/2.5/weather",
                          params={'q': city,
                                  'type': 'like', 'units': 'metric',
                                  'lang': 'ru', 'APPID': appid})
    data = result.json()
    bot.send_message(chat_id=update.message.chat_id,
                     text="conditions: {}".
                     format(data['weather'][0]['description']))
    bot.send_message(chat_id=update.message.chat_id,
                     text="temp: {} °C".format(data['main']['temp']))
    bot.send_message(chat_id=update.message.chat_id,
                     text="temp_min: {} °C".format(data['main']['temp_min']))
    bot.send_message(chat_id=update.message.chat_id,
                     text="temp_max: {} °C".format(data['main']['temp_max']))


def main():
    updater = Updater("595682641:AAFsQbY0_rsf9sY33eizNuonrj38Eq8ZZb4")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(CommandHandler("caps", caps, pass_args=True))
    dp.add_handler(CommandHandler("weather", Weather, pass_args=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

