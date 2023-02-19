import logging
import os
import random
import telegram.error
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext, \
    ConversationHandler
# from text_generation import newsum
from revChatGPT.V1 import Chatbot

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', '8433'))
TELE_TOKEN = os.environ.get('TELE_TOKEN')


# def generate_text(input_sentence):
#     output = newsum(input_sentence)
#
#     return output

# Define Command Handlers
# def resume(update: Update, context: CallbackContext):
#     """Handler for /start command"""
#     input_sentence = update.message.reply_to_message
#     if not input_sentence:
#         print("input:", input_sentence)
#         update.message.reply_text("Rispondi a un messaggio con /riassunto per riassumerlo")
#     else:
#         input_sentence = update.message.reply_to_message["text"]
#         if len(input_sentence) < 800:
#             update.message.reply_text("Il testo è troppo corto.")
#         else:
#             print("input:", input_sentence)
#             update.message.reply_text("Sto riassumendo...")
#             output = newsum(input_sentence)[0]["summary_text"]
#             print(output)
#             update.message.reply_text(output)


chatbot = Chatbot(config={
    "email": f"{os.environ.get('chatgpt_login')}",
    "password": f"{os.environ.get('chatgpt_pw')}"
})


def chat_gpt_output_parser(prompt: str, update: Update, context: CallbackContext):
    reply = update.message.reply_text("Sto scrivendo...")
    gpt_out = ""
    for idx, data in enumerate(chatbot.ask(prompt)):
        gpt_out = data["message"]
        print(gpt_out)
        if gpt_out:
            if idx % 18 == 0:
                try:
                    context.bot.editMessageText(chat_id=update.message.chat_id,
                                                message_id=reply.message_id,
                                                text=gpt_out)
                except telegram.error.BadRequest:
                    pass
    try:
        context.bot.editMessageText(chat_id=update.message.chat_id,
                                    message_id=reply.message_id,
                                    text=gpt_out)
    except telegram.error.BadRequest:
        pass


def get_replied_message_text(update: Update):
    """Handler for /start command"""
    input_text = update.message.reply_to_message
    if not input_text:
        print("input:", input_text)
        update.message.reply_text("Rispondi a un messaggio con /riassunto per riassumerlo")
    else:
        input_text = update.message.reply_to_message["text"]
        return input_text


def summarize(update: Update, context: CallbackContext, mode: str = "rules"):  # "ml" / "rules"
    input_text = f"riassumi questo testo\n\n{get_replied_message_text(update)}"
    print("input:", input_text)
    print(update.message)
    chat_gpt_output_parser(input_text, update, context)


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