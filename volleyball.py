# -*- coding: utf-8 -*-
import time
import requests
import fake_useragent
import winsound
from tkinter import Tk, Label
from threading import Thread
from telegram.ext import Updater
from smsru_api import SmsRu
from decouple import config

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


# функция получения Content-Lenght любой страницы
def length_page(url_page):
    return int(session.get(url_page, stream=True).headers['Content-Length'])


# функция авторизации второго логина
def second_connection(url_reg):
    """user_second = fake_useragent.UserAgent().random
    header_second = {
      'user-agent': user_second
    }"""
    header_second = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
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
    print('Отправляемся на вторую регистрацию')
    # передача данных для авторизации
    session_second.post(LINK, data=data_second, headers=header_second).headers
    session_second.get(url_reg, headers=header)
    print('Вторая регистрация:', url_reg)


# функция регистрации на сайте
def registration():
    time.sleep(DELAY_REG)
    # регистрация на первой ожидаемой тренировке
    session.get(url_reg_week_train[0], headers=header)
    print('Регистрация на:', url_reg_week_train[0])
    second_connection(url_reg_week_train[0])
    for j in range(NUMBER_TRAINING - 1):
        # проверка наличия следующих тренировок кроме первой
        if checking_training(url_week_train[j + 1], triggering_status):
            # добавил задержку по времени регистрации на тренировках
            time.sleep(DELAY_REG * (j + 1))
            session.get(url_reg_week_train[j + 1], headers=header)
            print('Регистрация на:', url_reg_week_train[j + 1])
            second_connection(url_reg_week_train[j + 1])
            continue
    print('Регистрация завершена')


# функция для проигрывания мелодии при начале записи
def sound():
    winsound.PlaySound('sirena.wav', winsound.SND_FILENAME)


# функция для вывода с сообщение о начале записи
def window():
    window = Tk()
    window.geometry("1700x700")
    window.title("Volleyball")
    l2 = Label(window, font='Arial 48', text="ЗАПИСЬ!!!, ЗАПИСЬ!!!, ЗАПИСЬ!!!")
    l2.pack()
    # эта строка делает, чтобы окно выводилось поверх всех открытых окон
    window.attributes('-topmost', True)
    window.mainloop()


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
    print('Проверяю ', url_test)
    if triggering_status:
        while True:
            if length_page(url_test) - FAKE_LENGTH > DELTA_TRAINING:
                print('Тренировка: ', url_test, 'появилась')
                return True
            else:
                time.sleep(DELAY_CHECK)
                print('Проверяю ', url_test)
    else:
        for i in range(NUMBER_FIRST_CHECK):
            if length_page(url_test) - FAKE_LENGTH > DELTA_TRAINING:
                print('Тренировка: ', url_test, 'появилась')
                triggering_status = True
                return True
            else:
                time.sleep(DELAY_FIRST_CHECK)
                print('Проверяю ', url_test)
    print('Это ложное срабатывание')
    return False


# создание юзер агента
# user = fake_useragent.UserAgent().random
# header = {
#      'user-agent': user
# }
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}
# данные для авторизации на сайте
# здесь перевод кодировки логина
data = {
     'login_name': NAME_MAIN.encode('cp1251'),
     'login_password': PASSWORD_MAIN,
     'login': 'submit'

}
# открытие файла с номером последней тренировки
f = open('number.txt')
# последний номер документа с тренировкой
last_number = int(f.read())
print('Номер последней тренировки ', last_number)
f.close()
# определяем chat_id, token, и сообщение для отправки в телеграм
# при начале записи
CHAT_ID_TELEGRAM_FIRST = config('CHAT_ID_TELEGRAM_FIRST', default='')
TOKEN_TELEGRAM_FIRST = config('TOKEN_TELEGRAM_FIRST', default='')
MESSAGE_FIRST = 'Запись! Запись! Запись!'
# определяем chat_id, token группы в телеграм для служебных сообщений
CHAT_ID_TELEGRAM_SEC = config('CHAT_ID_TELEGRAM_SEC', default='')
TOKEN_TELEGRAM_SEC = config('TOKEN_TELEGRAM_SEC', default='')
# сообщение в телеграм о неполадках
MESSAGE_SEC = 'Что-то пошло не так!'

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
            print(i)
            # формирование списка адресов ожидаемых тренировок
            url_week_train.append(URL_TRAINING + str(last_number + 1 + i))
            # формирование списка адресов страницы регистрации первой ожидаемой
            # тренировки
            url_reg_week_train.append(URL_REG + str(last_number + 1 + i))
            print(url_week_train[i])
            print(url_reg_week_train[i])
        # создание сессии при подключении к сайту
        session = requests.Session()
        print('running')
        # передача данных для авторизации
        session.post(LINK, data=data, headers=header)
        # cохранение текущего значения длины страницы cо всеми тренировками
        current_length = length_page(URL_TRAINING_LIST)
        print('начальная длина -', current_length)
        # адрес последней существующей тренировки
        url_last = URL_TRAINING + str(last_number)
        print('адрес последней существующей тренировки', url_last)
        # печать  длины последней существующей тренировки
        print('Длина последней тренировки', length_page(url_last))
        # формирование адреса точно несуществуюещей тренировки
        url_fake = URL_TRAINING + str(last_number + 1 + DELTA_FAKE)
        print('адрес точно несуществующей тренировки', url_fake)
        # получение Content-Length страницы с точно несуществующей тренировкой
        FAKE_LENGTH = length_page(url_fake)
        # получение длины первой ожидаемой тренировки
        new_length_training = length_page(url_week_train[0])
        print(url_week_train[0],
              new_length_training,
              new_length_training - FAKE_LENGTH > DELTA_TRAINING)
        print('длина первой возможной тренировки', new_length_training)
        print('длина тренировки, которой точно не существует', FAKE_LENGTH)
        # цикл проверки изменения размеры страницы с тренировками
        while True:
            try:
                time.sleep(DELAY_LIST)
                # сохраняем новое значение длинны страницы с тренировками
                new_current_length = length_page(URL_TRAINING_LIST)
                print('новая длина', new_current_length)
                # функция возвращает локальное время в виде кортежа
                t = time.localtime()
                # функция преорбразует кортеж в строку с часами и минутами
                current_time = time.strftime("%H:%M:%S", t)
                # выводим время, старое и новое значение длины и их разницу
                print(current_time, ' ', new_current_length,
                      '-', current_length, '=',
                      new_current_length - current_length)
                # выводит булево значение разницы и заданой дельты
                print(new_current_length - current_length
                      > DELTA_LIST)
                if new_current_length - current_length > DELTA_LIST:
                    print('произошли изменения')
                    # запуск функции проверки наличия тренировки
                    if checking_training(url_week_train[0], triggering_status):
                        # запуск потока воспроизведения звука
                        th1 = Thread(target=sound)
                        # запуск потока появления всплывающего окна
                        th2 = Thread(target=window)
                        th1.start()
                        th2.start()
                        # запуск функции отправки СМС
                        send_SMS()
                        # запуск функции отправки сообщения в Телеграмм
                        message(CHAT_ID_TELEGRAM_FIRST, TOKEN_TELEGRAM_FIRST,
                                MESSAGE_FIRST)
                        # запуск функции регистрации
                        registration()
                        # меняем номер последнее тренировки
                        last_number += NUMBER_TRAINING
                        print('Номер последней тренировки изменился',
                              last_number)
                        # запись в файл нового значения
                        # последней тренировки
                        f = open('number.txt', 'w')
                        f.write(str(last_number))
                        f.close()
                        print('Номер записался в файл')
                        break
                    else:
                        print('Продолжаем ждать изменения')
                current_length = new_current_length
                print('Новая длина сейчас =', current_length)
            except Exception as e:
                message(CHAT_ID_TELEGRAM_SEC, TOKEN_TELEGRAM_SEC, MESSAGE_SEC)
                print('error', e)
    except Exception:
        print('Что то пошло не так')
