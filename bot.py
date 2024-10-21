import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext


load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hej! I am Random Earnings Bot.')

if __name__ == '__main__':
    updater = Updater(TOKEN)
    dispather = updater.dispather
    dispather.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()