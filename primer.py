# -*- coding: utf-8 -*-
import time
import requests
import fake_useragent
import winsound
from tkinter import Tk, Label
from threading import Thread
from telegram.ext import Updater
from smsru_api import SmsRu

# адрес сайта
LINK = 'http://sportforus.ru/'
# адрес списка тренировок
URL_TRAINING_LIST = 'http://sportforus.ru/wv/training/list'
# адрес документа о тренировке
URL_TRAINING = 'http://sportforus.ru/wv/training/'
# начало строки документа для регистрации
URL_REG = 'http://sportforus.ru/wv/training/reg/'
# последний номер документа с тренировкой
LAST_NUMBER = 3729
# Content-Length страницы с несуществующей тренировкой
FAKE_LENGTH = 9278
# Дельта изменений длины контента списка всех тренировок
DELTA_LIST = 7
# Дельта изменений длины контента после размещений тренировки на сайте
DELTA_TRAINING = 100

# функция регистрации второго пользователя
def second_connection():
    URL_reg_second = URL_REG  + str(LAST_NUMBER + 1)
    # создание юзер агента
    user_second = fake_useragent.UserAgent().random
    header_second = {
      'user-agent': user_second
    }
    # данные для авторизации на сайте
    name_second = 'Полина Махнёва'
    data_second = {
         'login_name': name_second.encode('cp1251'),  # здесь перевод кодировки логина
         'login_password': 'v3z8b1a73r9',
         'login': 'submit'
    }
    # создание второй сессии при подключении к сайту
    session_second = requests.Session()
    print('Отправляемся на регистрацию Полины')
    # передача данных для авторизации
    session_second.post(LINK, data=data_second, headers=header_second).headers
    for i in range(6):
       # запрос для записи на тренировку
        session_second.get(URL_reg_second, headers=header)
        print('Регистрация Полины:', URL_reg_second)
        # составление адреса слудующей тренировки
        URL_reg_second = URL_REG + str(LAST_NUMBER + i + 2)
        time.sleep(3)


# функция регистрации на сайте
def registration(first_URL):
    for i in range(6):
        # запрос для записи на тренировку
        session.get(first_URL, headers=header)
        print('Моя регистрация:', first_URL)
        # составление адреса слудующей тренировки
        first_URL = URL_REG + str(LAST_NUMBER + i + 2)
        time.sleep(10)
    print('Функция моей регистрации завершилась')
    # запуск потока второой регистрации
    th3 = Thread(target=second_connection)
    th3.start()


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


# функция для отправки сообщения о начале записи в телеграм
def message():
    chat_id = '-829440234'
    updater = Updater("5520994198:AAFkYOFAi6rNdvLiM6hfYVbYU59OYD3b-3c",
                      use_context=True)
    message = "Возможно началась запись"
    updater.bot.send_message(chat_id=chat_id, text=message)


# функция для отправки SMS о начале записи на номер телефона
def send_SMS():
    sms_ru = SmsRu('C51BE417-745B-C0B4-F80D-A71F29127C55')
    sms_ru.send('9000905976', '9227050474', message='ЗАПИСЬ!!!! ЗАПИСЬ!!!! ЗАПИСЬ!!!!')


# создание юзер агента
user = fake_useragent.UserAgent().random
header = {
      'user-agent': user
}
# данные для авторизации на сайте
name = 'Олеег'
data = {
     'login_name': name.encode('cp1251'),  # здесь перевод кодировки логина
     'login_password': 'a5k69mf223y',
     'login': 'submit'

}

while True:
    try:
        # создание сессии при подключении к сайту
        session = requests.Session()
        print('running')
        # передача данных для авторизации
        session.post(LINK, data=data, headers=header).headers

        # получение заголовоков страницы с тренировками
        headers_training_list = session.get(URL_TRAINING_LIST,
                                            stream=True).headers
        # cохранение текущего значения размера страницы cо всеми тренировками
        current_length = headers_training_list['Content-Length']

        print('начальная длина -', current_length)

        # адрес  первой ожидаемой тренировки
        # например 'http://sportforus.ru/wv/training/3723'
        new_URL_training = URL_TRAINING + str(LAST_NUMBER + 1)
        # получение длины первой ожидаемой тренировки
        new_length_training = session.get(
            new_URL_training, stream=True
            ).headers['Content-Length']
        print(new_URL_training,
              new_length_training,
              int(new_length_training) - FAKE_LENGTH > DELTA_TRAINING)

        # цикл проверки изменения размеры страницы с тренировками
        while True:
            try:
                time.sleep(30)
                headers_training_list = session.get(URL_TRAINING_LIST,
                                                    stream=True).headers
                new_current_length = headers_training_list['Content-Length']
                print('новая длина', new_current_length)
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                print(current_time, ' ', int(new_current_length),
                      '-', int(current_length), '=',
                      int(new_current_length) - int(current_length))
                print((int(new_current_length) - int(current_length)
                       ) <= DELTA_LIST)
                if int(new_current_length) - int(current_length) <= DELTA_LIST:
                    continue
                else:
                    print('произошли изменения')
                    # запуск потока воспроизведения звука
                    th1 = Thread(target=sound)
                    # запуск потока появления всплывающего окна
                    th2 = Thread(target=window)
                    th1.start()
                    th2.start()
                    # запуск функции отправки СМС
                    send_SMS()
                    # запуск функции отправки сообщения в Телеграмм
                    message()
                    time.sleep(10)
                    # проверка длины страницы с несуществующей тренировкой
                    if int(new_length_training) - FAKE_LENGTH > DELTA_TRAINING:
                        print('Ожидаемая тренировка появилась, ее длина =', new_length_training)
                        # адрес страницы регистрации на тренировке
                        new_URL_reg = URL_REG + str(LAST_NUMBER + 1)
                        print('Отправляемся на автоматическую регистрацию')
                        registration(new_URL_reg)
                        headers_training_list = session.get(
                                              URL_TRAINING_LIST, stream=True
                                              ).headers
                        current_length = headers_training_list[
                                       'Content-Length']
                    break
            except Exception as e:
                print('error', e)
    except Exception:
        print('Что то пошло не так')
