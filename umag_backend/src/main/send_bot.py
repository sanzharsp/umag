from dotenv import load_dotenv
import os
import telebot

load_dotenv()
bot_token = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(bot_token, parse_mode=None)

def send_telegram_message(chat_id, message):
    try:
        bot.send_message(chat_id, message, parse_mode="Markdown")

    except Exception as e:
        print(e)
