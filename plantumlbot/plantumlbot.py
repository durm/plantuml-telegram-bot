import logging
import os

import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from utils import get_uml, deflate_and_encode

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text("Hi! It's a bot. Recieve message return picture =)")


def help(bot, update):
    update.message.reply_text('Help! Take a look http://plantuml.com/PlantUML_Language_Reference_Guide.pdf')


def echo(bot, update):
    uml = get_uml(update.message.text)
    if uml:
        url = "http://plantuml:8080/img/{}".format(deflate_and_encode(uml.encode()))
        resp = requests.get(url, stream=True)
        resp.raise_for_status()
        bot.sendPhoto(update.message.chat_id, resp.raw)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    token = os.getenv("PLANTUMLBOT", None)
    assert token, "can't start without token"
    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()