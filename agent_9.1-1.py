import os, sys
import telebot
from dotenv import load_dotenv

load_dotenv()

telegram_token = os.getenv("TELEGRAM_TOKEN") or sys.exit("Ошибка: в файле .env отсутствует TELEGRAM_TOKEN")

bot = telebot.TeleBot(telegram_token)


@bot.message_handler(func=lambda msg: True)
def echo(message):
    bot.reply_to(message, message.text)


bot.polling()