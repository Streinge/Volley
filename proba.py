import time
from telegram.ext import Updater
chat_id = '1082504319'
updater = Updater("5579939015:AAFJq9Sz0TSZp-NFxRr9_K8QE9Z7dsshymY",
                   use_context=True)
message = "Не обращай внимание - это тестирование"
for i in range(10):
    updater.bot.send_message(chat_id=chat_id, text=message)
    time.sleep(10)