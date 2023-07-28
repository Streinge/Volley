# -*- coding: utf-8 -*-
import requests
from fake_useragent import UserAgent
from telegram.ext import Updater
from smsru_api import SmsRu
from decouple import config
from time import localtime, sleep, strftime

# адрес сайта
LINK = config('LINK', default='')
# адрес списка тренировок
URL_TRAINING_LIST = config('URL_TRAINING_LIST', default='')
# адрес документа о тренировке
URL_TRAINING = config('URL_TRAINING', default='')
# начало строки документа для регистрации
URL_REG = config('URL_REG', default='')
# Дельта изменений длины контента списка всех тренировок
DELTA_LIST = 7
# Дельта изменений длины контента после размещений тренировки на сайте
DELTA_TRAINING = 100
# Количество тренировок в неделе
NUMBER_TRAINING = 7
# задержка по времени при регистрации тренировок, секунд
DELAY_REG = 7
# задержка по времени между проверками наличия тренировки в первый раз
DELAY_FIRST_CHECK = 10
# задержка по времени между проверками наличия тренировки
DELAY_CHECK = 3
# задержка по времени между опросами об изменениях страницы с тренировками
DELAY_LIST = 30
# Основной логин
NAME_MAIN = config('NAME_MAIN', default='')
# Пароль к основному логину
PASSWORD_MAIN = config('PASSWORD_MAIN', default='')
# Второй логин
NAME_SECOND = config('NAME_SECOND', default='')
PASSWORD_SECOND = config('PASSWORD_SECOND', default='')
# число проверок тренировок при первой сработке
NUMBER_FIRST_CHECK = 3
# дельта для проверки точно несуществующе тренировки
# то есть сколько прибавить к номеру последней тренировки
# чтобы точно получить нереальный номер
DELTA_FAKE = 100
# сдвиг по времени с учетом часового пояса
OFFSET_UTC = 0
# значение часа локального время начало работы
START_HOUR = 8
# значение часа локального время начало работы
FINISH_HOUR = 20


# функция получения Content-Lenght любой страницы
def length_page(url_page):
    return int(session.get(url_page, stream=True).headers['Content-Length'])


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


# функция авторизации второго логина
def second_connection(url_reg):
    global week_day
    user_second = UserAgent().random
    header_second = {
      'user-agent': user_second
    }
    # данные для авторизации на сайте
    # здесь перевод кодировки логина
    data_second = {
         'login_name': NAME_SECOND.encode('cp1251'),
         'login_password': PASSWORD_SECOND,
         'login': 'submit'
    }
    # создание второй сессии при подключении к сайту
    session_second = requests.Session()
    write_status_messages('Go on second registration %s' % url_reg,
                          week_day)
    # передача данных для авторизации
    session_second.post(LINK, data=data_second, headers=header_second).headers
    session_second.get(url_reg, headers=header)


# функция регистрации на сайте
def registration():
    global week_day
    sleep(DELAY_REG)
    # регистрация на первой ожидаемой тренировке
    session.get(url_reg_week_train[0], headers=header)
    write_status_messages('Registration on: %s' % url_reg_week_train[0],
                          week_day)
    second_connection(url_reg_week_train[0])
    for j in range(NUMBER_TRAINING - 1):
        # проверка наличия следующих тренировок кроме первой
        if checking_training(url_week_train[j + 1], triggering_status):
            # добавил задержку по времени регистрации на тренировках
            sleep(DELAY_REG * (j + 1))
            session.get(url_reg_week_train[j + 1], headers=header)
            write_status_messages('Registration on:: %s'
                                  % url_reg_week_train[j + 1], week_day)
            second_connection(url_reg_week_train[j + 1])
            continue
    write_status_messages('Registration is over!:', week_day)


# функция для отправки сообщения  в телеграм
def message(chat_id, token, message):
    updater = Updater(token, use_context=True)
    updater.bot.send_message(chat_id=chat_id, text=message)


# функция для отправки SMS о начале записи на номер телефона
def send_SMS():
    TOKEN_SMS = config('TOKEN_SMS', default='')
    sms_ru = SmsRu(TOKEN_SMS)
    PHONE_NUMBER_1 = config('PHONE_NUMBER_1', default='')
    PHONE_NUMBER_2 = config('PHONE_NUMBER_2', default='')
    sms_ru.send(PHONE_NUMBER_1, PHONE_NUMBER_2,
                message='ЗАПИСЬ!!!! ЗАПИСЬ!!!! ЗАПИСЬ!!!!')


# функция проверки наличия тренировки
def checking_training(url_test, triggering_status):
    write_status_messages('Check %s' % url_test, week_day)
    if triggering_status:
        while True:
            if length_page(url_test) - FAKE_LENGTH > DELTA_TRAINING:
                write_status_messages('The training appeared: %s' % url_test,
                                      week_day)
                return True
            else:
                sleep(DELAY_CHECK)
                write_status_messages('Check %s' % url_test, week_day)
    else:
        for i in range(NUMBER_FIRST_CHECK):
            if length_page(url_test) - FAKE_LENGTH > DELTA_TRAINING:
                write_status_messages('The training appeared: %s' % url_test,
                                      week_day)
                triggering_status = True
                return True
            else:
                sleep(DELAY_FIRST_CHECK)
                write_status_messages('Check %s' % url_test, week_day)
    print('This is a false positive')
    return False

def send_into_telegram_current_time(send_message):
    current_year = localtime().tm_year
    current_month = localtime().tm_mon
    current_day = localtime().tm_mday
    str_temp = (str(current_day) + '.' +
                str(current_month) + '.' +
                str(current_year) + ' ' +
                str(current_time) + ' ' + send_message)
    message(CHAT_ID_TELEGRAM_SEC, TOKEN_TELEGRAM_SEC, str_temp)
    write_status_messages(str_temp, week_day)


# создание юзер агента
user = UserAgent().random
header = {
      'user-agent': user
}
# данные для авторизации на сайте
# здесь перевод кодировки логина
data = {
     'login_name': NAME_MAIN.encode('cp1251'),
     'login_password': PASSWORD_MAIN,
     'login': 'submit'

}
# в начале работы программы получаем значение текущего дня
with open('day_status.txt', 'r') as day_file:
    day_string = day_file.read()
# проверка условия, если файл пустой то присваивается ноль
# чтобы не было ошибки int()
if day_string == '':
    day_status = 0
else:
    day_status = int(day_string)
# получаем номер дня недели
# день недели плюс 1, потому что по умолчанию начинается с 0
week_day = week_day = localtime().tm_wday + 1
# открытие файла с номером последней тренировки
f = open('number.txt')
# последний номер документа с тренировкой
last_number = int(f.read())
f.close()
write_status_messages('Nunber of last training  %s' % last_number, week_day)
# определяем chat_id, token, и сообщение для отправки в телеграм
# при начале записи
CHAT_ID_TELEGRAM_FIRST = config('CHAT_ID_TELEGRAM_FIRST', default='')
TOKEN_TELEGRAM_FIRST = config('TOKEN_TELEGRAM_FIRST', default='')
MESSAGE_FIRST = 'Запись! Запись! Запись!'
# определяем chat_id, token группы в телеграм для служебных сообщений
CHAT_ID_TELEGRAM_SEC = config('CHAT_ID_TELEGRAM_SEC', default='')
TOKEN_TELEGRAM_SEC = config('TOKEN_TELEGRAM_SEC', default='')
# сообщение в телеграм о неполадках
MESSAGE_SEC = 'Something went wrong!'

while True:
    try:
        # задает переменную состояния, появилась или нет ожидаемая тренировка
        triggering_status = False
        # список адресов ожидаемых тренировок
        url_week_train = []
        # список адресов страниц регистрации ожидаемых тренировок
        url_reg_week_train = []
        # создание списка ожидаемых тренировок на ближайшую неделю
        # и создание списка страниц регистрации ожидаемых тренировок
        for i in range(NUMBER_TRAINING):
            # формирование списка адресов ожидаемых тренировок
            url_week_train.append(URL_TRAINING + str(last_number + 1 + i))
            # формирование списка адресов страницы регистрации первой ожидаемой
            # тренировки
            url_reg_week_train.append(URL_REG + str(last_number + 1 + i))
            write_status_messages(url_week_train[i], week_day)
            write_status_messages(url_reg_week_train[i], week_day)
        # создание сессии при подключении к сайту
        session = requests.Session()
        # передача данных для авторизации
        session.post(LINK, data=data, headers=header)
        # cохранение текущего значения длины страницы cо всеми тренировками
        current_length = length_page(URL_TRAINING_LIST)
        write_status_messages('Initial length - %s' % current_length,
                              week_day)
        # адрес последней существующей тренировки
        url_last = URL_TRAINING + str(last_number)
        write_status_messages(
            'URL of the last existing workout %s' % url_last, week_day)
        # печать  длины последней существующей тренировки
        write_status_messages(
            'The length of the last workout %s' % length_page(url_last),
            week_day)
        # формирование адреса точно несуществуюещей тренировки
        url_fake = URL_TRAINING + str(last_number + 1 + DELTA_FAKE)
        write_status_messages(
            'the URL of a non-existent workout for sure %s' % url_fake,
            week_day)
        # получение Content-Length страницы с точно несуществующей тренировкой
        FAKE_LENGTH = length_page(url_fake)
        # получение длины первой ожидаемой тренировки
        new_length_training = length_page(url_week_train[0])
        str_temp = (url_week_train[0] + ' length ' + str(new_length_training)
                    + ' ' + str((new_length_training - FAKE_LENGTH) >
                                DELTA_TRAINING))
        write_status_messages(str_temp, week_day)
        write_status_messages('length of the first possible workout %s' %
                              new_length_training, week_day)
        write_status_messages(
            'the length of the shadow, which definitely does not exist %s' %
            FAKE_LENGTH, week_day)
        # hour_status переменная, которая хранит значение часа на которое 
        # уже выводилось значение о печати статус сообщения в Телеграм
        hour_status = 0
        # цикл проверки изменения размеры страницы с тренировками
        while True:
            try:
                message(CHAT_ID_TELEGRAM_SEC, TOKEN_TELEGRAM_SEC, 'GO! GO! GO!')
                # получаем номер дня недели
                # день недели плюс 1, потому что по умолчанию начинается с 0
                week_day = localtime().tm_wday + 1
                # получаем текущюу минуту локального времени
                # current_minute = localtime().tm_min
                # fixed_minute = current_minute
                # здесь реализовал бесконечный цикла с проверкой времени:
                # программа начинает работу 8 часов утра  и заканчивает в 20 часов
                # минуты но дальше продолжает работать и ждать по идее утра
                while True:
                    # получаем текущий час локального времени
                    current_hour = localtime().tm_hour + OFFSET_UTC
                    # current_minute = localtime().tm_min
                    if (current_hour >= START_HOUR) and (current_hour <= FINISH_HOUR):
                    # if (current_minute >= fixed_minute + 1) and (current_minute
                    #                                             < fixed_minute
                    #                                             + 5):
                        # сохраняем значение длины страницы с тренировками
                        new_current_length = length_page(URL_TRAINING_LIST)
                        write_status_messages('New length %s' %
                                              new_current_length, week_day)
                        sleep(DELAY_LIST)
                        # функция возвращает локальное время в виде кортежа
                        t = localtime()
                        # функция преорбразует кортеж в строку с часами и
                        # минутами
                        current_time = strftime("%H:%M:%S", t)
                        # выводим время, старое и новое значение длины
                        # и их разницу
                        str_temp = (str(current_time) + ' ' +
                                    str(new_current_length) + '-' +
                                    str(current_length) + '=' +
                                    str(new_current_length - current_length))
                        write_status_messages(str_temp, week_day)
                        # условие чтобы один раз в час печаталось сообщение 
                        # в Телеграмм о том что программа работает - изменений нет
                        if current_hour != hour_status:
                            send_into_telegram_current_time('We are waiting for new training sessions')
                            hour_status = current_hour
                        # выводит булево значение разницы и заданой дельты
                        write_status_messages(str(new_current_length -
                                              current_length > DELTA_LIST),
                                              week_day)
                        if new_current_length - current_length > DELTA_LIST:
                            write_status_messages('There have been changes',
                                                  week_day)
                            # запуск функции проверки наличия тренировки
                            if checking_training(url_week_train[0],
                                                 triggering_status):
                                # запуск функции отправки СМС
                                send_SMS()
                                # запуск функции отправки сообщения в Телеграмм
                                message(CHAT_ID_TELEGRAM_FIRST,
                                        TOKEN_TELEGRAM_FIRST, MESSAGE_FIRST)
                                # запуск функции регистрации
                                registration()
                                # меняем номер последнее тренировки
                                last_number += NUMBER_TRAINING
                                str_temp = ('Number last training is changed '
                                            + str(last_number))
                                write_status_messages(str_temp, week_day)
                                # запись в файл нового значения
                                # последней тренировки
                                f = open('number.txt', 'w')
                                f.write(str(last_number))
                                f.close()
                                write_status_messages(
                                    'Number writed at file %s' % week_day)
                                break
                            else:
                                write_status_messages(
                                    'Continue wait changes %s' % week_day)
                        current_length = new_current_length
                        write_status_messages(
                            'New length now = %s' % current_length, week_day)
                    else:
                        # получаем текущий час локального времени
                        current_hour = localtime().tm_hour + OFFSET_UTC
                        # каждые 60 секунд проверяется статус рабочего времени
                        sleep(60)
                        if current_hour != hour_status:
                            send_into_telegram_current_time('Waiting for the morning')
                            hour_status = current_hour
            except Exception as e:
                message(CHAT_ID_TELEGRAM_SEC, TOKEN_TELEGRAM_SEC, MESSAGE_SEC)
                write_status_messages('error %s' % e, week_day)
    except Exception:
        write_status_messages('Something went wrong', week_day)
