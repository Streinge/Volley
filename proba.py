import time
from telegram.ext import Updater
chat_id = '-829440234'
updater = Updater("5520994198:AAFkYOFAi6rNdvLiM6hfYVbYU59OYD3b-3c",
                   use_context=True)
message = "Полина! Не обращай внимание - это тестирование"
for i in range(10):
    updater.bot.send_message(chat_id=chat_id, text=message)
    time.sleep(10)