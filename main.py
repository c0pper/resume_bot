import logging
import os
import random
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext, \
    ConversationHandler

# from text_generation import newsum
from rules_summary import rules_summary

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', '8433'))
TELE_TOKEN = os.environ.get('TELE_TOKEN')
MIN_TXT_LEN = 800



# Define Command Handlers
def get_input_text(update: Update):
    """Handler for /start command"""
    input_text = update.message.reply_to_message
    if not input_text:
        print("input:", input_text)
        update.message.reply_text("Rispondi a un messaggio con /riassunto per riassumerlo")
    else:
        input_text = update.message.reply_to_message["text"]
        return input_text


def summarize(update: Update, context: CallbackContext,  mode: str = "rules"):  # "ml" / "rules"
    input_text = get_input_text(update)

    if len(input_text) < MIN_TXT_LEN:
        update.message.reply_text("Il testo è troppo corto.")
    else:
        print("input:", input_text)
        print(update.message)
        update.message.reply_text("Sto riassumendo...")

        if mode == "ml":
            # output = ML_resume(input_text, update)
            # print(output)
            # update.message.reply_text
            raise NotImplementedError
        elif mode == "rules":
            output = rules_summary(input_text)
            print(output)
            update.message.reply_text(output)
        else:
            raise NotImplementedError


# def ML_resume(input_text: str, update: Update):
#     output = newsum(input_text)[0]["summary_text"]
#     return output


def main():
    """starting bot"""
    updater = Updater(TELE_TOKEN, use_context=True)

    # getting the dispatchers to register handlers
    dp = updater.dispatcher
    # registering commands
    dp.add_handler(CommandHandler("riassunto", summarize))

    # starting the bot
    updater.start_polling()
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=PORT,
    #                       url_path=TELE_TOKEN,
    #                       webhook_url=HEROKU_URL + TELE_TOKEN)
    # updater.idle()


if __name__ == '__main__':
    main()