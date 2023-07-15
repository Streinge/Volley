from time import localtime, sleep, strftime
# from decouple import config
# from telegram.ext import Updater
# CHAT_ID_TELEGRAM_SEC = config('CHAT_ID_TELEGRAM_SEC', default='')
# TOKEN_TELEGRAM_SEC = config('TOKEN_TELEGRAM_SEC', default='')
# updater = Updater(token=TOKEN_TELEGRAM_SEC, use_context=True)
# message = "Не обращай внимание - это тестирование"
# for i in range(10):
#     updater.bot.send_message(chat_id=CHAT_ID_TELEGRAM_SEC, text=message)
#     time.sleep(10)

# функция записывает в файл логи
# на вход получает сообщение записываемое и день недели
# 1 - это понедельник, 7 - это воскресенье
# результ - строка записанная в фалы логов
# запись ведется в 7 файлов, каждый соответствует дню недели


def write_status_messages(message, day):
    # переменная с именем файла для хранения переменной текущего дня
    global day_file
    # переменная со значением текущего дня
    global day_status
    # имя файла формируется в зависимости от дня недели
    file_name = 'output_%s.txt' % day
    # проверяется, если день недели изменился, то стирается
    # файл за прошлую неделю и меняется значение текущего дня
    # и новое значение записывается в файл (на случай внезапной остановки)
    if day != day_status:
        day_status = day
        output_file = open(file_name, 'w').close()
        with open('day_status.txt', 'w') as day_file:
            day_file.write(str(day))
    # проводится запись в конец файла с переводом строки (построчно)
    with open(file_name, 'a') as output_file:
        output_file.write('\n' + message)


# в начале работы программы получаем значение текущего дня
with open('day_status.txt', 'r') as day_file:
    day_string = day_file.read()
# проверка условия, если файл пустой то присваивается ноль
# чтобы не было ошибки int()
if day_string == '':
    day_status = 0
else:
    day_status = int(day_string)


# 1.хочу сделать чтобы программа работала только с 8 до 20 часов по местному
# времени в остальное время не висела на сервере волейбольном
# 2.каждый час отправляла сообщение о состоянии работы

current_year = localtime().tm_year
current_month = localtime().tm_mon
current_day = localtime().tm_mon
current_hour = localtime().tm_hour
# получаем номер дня недели
# день недели плюс 1, потому что по умолчанию начинается с 0
week_day = localtime().tm_wday + 1
# получаем текущюу минуту локального времени
current_minute = localtime().tm_min
fixed_minute = current_minute


# здесь реализовал бесконечный цикла с проверкой времени по минутам
# это аналог того, что делается по часам
# программа начинает работу через минуту и заканчивает через 2 минуты
# но дальше продолжает работать и ждать по идее утра, когда будет 8 часов
# Это по замыслу
while True:
    if (current_minute >= fixed_minute + 1) and (current_minute <
                                                 fixed_minute + 2):
        print('Начали работать')
        day = week_day
        for i in range(5):
            # функция возвращает локальное время в виде кортежа
            t = localtime()
            # функция преорбразует кортеж в строку с часами и минутами
            current_time = strftime("%H:%M:%S", t)
            write_status_messages(current_time, day)
            sleep(1)

        day = day + 1
        for i in range(5):
            # функция возвращает локальное время в виде кортежа
            t = localtime()
            # функция преорбразует кортеж в строку с часами и минутами
            current_time = strftime("%H:%M:%S", t)
            write_status_messages(current_time, day)
            sleep(1)

        day = day + 1

        for i in range(5):
            # функция возвращает локальное время в виде кортежа
            t = localtime()
            # функция преорбразует кортеж в строку с часами и минутами
            current_time = strftime("%H:%M:%S", t)
            write_status_messages(current_time, day)
            sleep(1)

        current_minute = localtime().tm_min
    else:
        sleep(1)
        current_minute = localtime().tm_min
        print('Ждем,', current_minute)
