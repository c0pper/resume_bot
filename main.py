import logging
import os
import random
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext, \
    ConversationHandler
from text_generation import newsum

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', '8433'))
TELE_TOKEN = os.environ.get('TELE_TOKEN')


def generate_text(input_sentence):
    output = newsum(input_sentence)

    return output


# Define Command Handlers
def resume(update: Update, context: CallbackContext):
    """Handler for /start command"""
    input_sentence = update.message.reply_to_message
    if not input_sentence:
        print("input:", input_sentence)
        update.message.reply_text("Rispondi a un messaggio con /riassunto per riassumerlo")
    else:
        input_sentence = update.message.reply_to_message["text"]
        print("input:", input_sentence)
        update.message.reply_text("Sto riassumendo...")
        output = newsum(input_sentence)[0]["summary_text"]
        print(output)
        update.message.reply_text(output)


def main():
    """starting bot"""
    updater = Updater(TELE_TOKEN, use_context=True)

    # getting the dispatchers to register handlers
    dp = updater.dispatcher
    # registering commands
    dp.add_handler(CommandHandler("riassunto", resume))

    # starting the bot
    updater.start_polling()
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=PORT,
    #                       url_path=TELE_TOKEN,
    #                       webhook_url=HEROKU_URL + TELE_TOKEN)
    # updater.idle()


if __name__ == '__main__':
    main()