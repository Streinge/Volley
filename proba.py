import time
from decouple import config
from telegram.ext import Updater


# CHAT_ID_TELEGRAM_SEC = config('CHAT_ID_TELEGRAM_SEC', default='')
# TOKEN_TELEGRAM_SEC = config('TOKEN_TELEGRAM_SEC', default='')
# updater = Updater(token=TOKEN_TELEGRAM_SEC, use_context=True)
# message = "Не обращай внимание - это тестирование"
# for i in range(10):
#     updater.bot.send_message(chat_id=CHAT_ID_TELEGRAM_SEC, text=message)
#     time.sleep(10)

# количестов строк, хранимых в файле информации о работе программы output.txt
OUTPUT_STRING_NUMBER = 3
# имя файла выходных данных о работае программы
OUTPUT_FILE_CONST = 'output_0.txt'

day_status

output_file = open(OUTPUT_FILE_CONST, 'w').close()
def write_status_messages(message, day):
    if day_status != day:

    file_name = 'output_%s.txt' % day
    with open(file_name, 'a') as output_file:
        output_file.write('\n' + message)


f = open('day_status.txt')

day_status = int(f.read())
f.close()



day = 1
for i in range(10):
    write_status_messages('Это сообщение состояния', day, day_status)
day_status = day_status + 1
with open('day_status.txt') as f:    
day = 2
for i in range(10):
    write_status_messages('Это сообщение состояния', day, day_status)
day_status = day_status + 1
day = 3
for i in range(10):
    write_status_messages('Это сообщение состояния', day, day_status)


