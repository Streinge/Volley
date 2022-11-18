from telegram.ext import Updater
from smsru_api import SmsRu
chat_id = '-829440234'
updater = Updater("5520994198:AAFkYOFAi6rNdvLiM6hfYVbYU59OYD3b-3c",
                 use_context=True)
message = "Возможно началась запись"
updater.bot.send_message(chat_id=chat_id, text=message)
sms_ru = SmsRu('C51BE417-745B-C0B4-F80D-A71F29127C55')
sms_ru.send('9000905976', message='ЗАПИСЬ!!!! ЗАПИСЬ!!!! ЗАПИСЬ!!!!')