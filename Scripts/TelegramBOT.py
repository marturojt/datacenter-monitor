"""
BOT de telegram para leer la temperatura del SITE de una base de datos de mysql
"""
import logging
import json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from data import keyTelegram
from db import dbOperations

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    db = dbOperations()
    dbQueryStart = "SELECT idtbMetodosBot, nombreMetodo FROM tbMetodosBot;"
    resultadoQueryStart = db.fetch(dbQueryStart)
    keyboard = []
    for key in resultadoQueryStart:
        keyboard.append([InlineKeyboardButton(key['nombreMetodo'], callback_data=key['idtbMetodosBot'])])


    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Por favor seleccione una opción de temperatura:', reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    logging.info(query.data)

    db = dbOperations()
    dbQuery = "CALL spMetodosBOT({});".format(query.data)
    resultadoQueryTemp = db.fetch(dbQuery)
    query.edit_message_text(text="{nMetodo} = {temp} °C".format(nMetodo=resultadoQueryTemp[0]['metodo'], temp=resultadoQueryTemp[0]['temperatura']))


def help_command(update, context):
    update.message.reply_text(
        "Use /start para iniciar el bot y obtener opciones.")


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    TOKEN = keyTelegram.BOT_KEY
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
