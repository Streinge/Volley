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

# Content-Length страницы с несуществующей тренировкой
FAKE_LENGTH = 9278
# Дельта изменений длины контента списка всех тренировок
DELTA_LIST = 7
# Дельта изменений длины контента после размещений тренировки на сайте
DELTA_TRAINING = 100
# Количество тренировок в неделе
NUMBER_TRAINING = 7
# задержка по времени при регистрации тренировок, секунд
DELAY_REG = 10
# задержка по времени между проверками наличия тренировки в первый раз
DELAY_FIRST_CHECK = 10
# задержка по времени между проверками наличия тренировки
DELAY_CHECK = 3
# задержка по времени между опросами об изменениях страницы с тренировками
DELAY_LIST = 60
# Основной логин
NAME_MAIN = 'Ludmila'
# Пароль к основному логину
PASSWORD_MAIN = 'sokol15'
# число проверок тренировок при первой сработке
NUMBER_FIRST_CHECK = 3

# последний номер документа с тренировкой
last_number = 3736


# функция получения Content-Lenght любой страницы
def length_page(url_page):
    return int(session.get(url_page, stream=True).headers['Content-Length'])


# функция регистрации второго пользователя
def second_connection(url_reg):
    user_second = fake_useragent.UserAgent().random
    header_second = {
      'user-agent': user_second
    }
    # данные для авторизации на сайте
    name_second = 'Полина Махнёва'
    # здесь перевод кодировки логина
    data_second = {
         'login_name': name_second.encode('cp1251'),
         'login_password': 'v3z8b1a73r9',
         'login': 'submit'
    }
    # создание второй сессии при подключении к сайту
    session_second = requests.Session()
    print('Отправляемся на регистрацию Полины')
    # передача данных для авторизации
    session_second.post(LINK, data=data_second, headers=header_second).headers
    session_second.get(url_reg, headers=header)
    print('Регистрация Полины:', url_reg)


# функция регистрации на сайте
def registration():
    # регистрация на первой ожидаемой тренировке
    session.get(url_reg_week_train[0], headers=header)
    print('Регистрация на:', url_reg_week_train[0])
    second_connection(url_reg_week_train[0])
    for j in range(NUMBER_TRAINING - 1):
        # проверка наличия следующих тренировок кроме первой
        if checking_training(url_week_train[j+1], triggering_status):
            session.get(url_reg_week_train[j+1], headers=header)
            print('Регистрация на:', url_reg_week_train[j+1])
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
    sms_ru.send('9000905976', '9227050474',
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
user = fake_useragent.UserAgent().random
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


while True:
    try:
        # задает переменную состояния, появилась или нет ожидаемая тренировка
        triggering_status = False
        print('triggering_status =', triggering_status)
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
        # получение длины первой ожидаемой тренировки
        new_length_training = length_page(url_week_train[0])
        print(url_week_train[0],
              new_length_training,
              new_length_training - FAKE_LENGTH > DELTA_TRAINING)
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
                      <= DELTA_LIST)
                if new_current_length - current_length <= DELTA_LIST:
                    continue
                else:
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
                        message()
                        # запуск функции регистрации
                        registration()
                        last_number += NUMBER_TRAINING
                    break
            except Exception as e:
                print('error', e)
    except Exception:
        print('Что то пошло не так')
