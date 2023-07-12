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
OUTPUT_FILE_CONST = 'output_1.txt'


def write_status_messages(message, day):
    global day_file
    global day_status
    file_name = 'output_%s.txt' % day
    if day != day_status:
        day_status = day
        output_file = open(file_name, 'w').close()
        with open('day_status.txt', 'w') as day_file: 
            day_file.write(str(day))
   
    with open(file_name, 'a') as output_file:
        output_file.write('\n' + message)
        


with open('day_status.txt', 'r') as day_file:
    day_string = day_file.read()
if day_string == '':
    day_status = 0
else:
    day_status = int(day_string)

test = 35
day = 1
for i in range(10):
    write_status_messages('Это сообщение состояния ', day)
           
day = 2
for i in range(10):
    write_status_messages('Это сообщение состояния', day)

day = 3

for i in range(10):
    write_status_messages('Это сообщение состояния', day)

