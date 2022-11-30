import time
from decouple import config
from telegram.ext import Updater


CHAT_ID_TELEGRAM_SEC = config('CHAT_ID_TELEGRAM_SEC', default='')
TOKEN_TELEGRAM_SEC = config('TOKEN_TELEGRAM_SEC', default='')
updater = Updater(token=TOKEN_TELEGRAM_SEC, use_context=True)
message = "Не обращай внимание - это тестирование"
for i in range(10):
    updater.bot.send_message(chat_id=CHAT_ID_TELEGRAM_SEC, text=message)
    time.sleep(10)