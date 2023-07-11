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
OUTPUT_FILE_CONST = 'output.txt'

output_file = open(OUTPUT_FILE_CONST, 'a')

def write_status_messages(message):
    global output_file
    global string_counter
    output_file.write('\n' + message)
    string_counter =+ 1
    # if string_counter > OUTPUT_STRING_NUMBER:
        


string_counter = 0
open(OUTPUT_FILE_CONST, 'w').close()

output_file = open(OUTPUT_FILE_CONST, 'a')


write_status_messages('Привет 1')
write_status_messages('Привет 2')

output_file.close()

# output_file.seek(0)

output_file = open(OUTPUT_FILE_CONST, 'w')

write_status_messages('Привет 3')

output_file.close()

# for i in range(5):
#     write_status_messages('\nПривет %s' %i)



# for i in range(5):
#     write_status_messages('\nПривет %s' %i) 