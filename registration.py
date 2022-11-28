# -*- coding: utf-8 -*-
import time
import requests
import fake_useragent

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
last_number = 3729

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



user = fake_useragent.UserAgent().random

header = {
      'user-agent': user
}

name = 'Ludmila'

data = {
     'login_name': name.encode('cp1251'),
     'login_password': 'sokol15',
     'login': 'submit'
}

print('running')
# список адресов ожидаемых тренировок
url_week_train = []
# список адресов страниц регистрации ожидаемых тренировок
url_reg_week_train = []

session = requests.Session()
# передача данных для авторизации
session.post(LINK, data=data, headers=header)
# создание списка ожидаемых тренировок на ближайшую неделю
# и создание списка страниц регистрации ожидаемых тренировок
for i in range(NUMBER_TRAINING):
    # формирование списка адресов ожидаемых тренировок
    url_week_train.append(URL_TRAINING + str(LAST_NUMBER + 1 + i))
    # формирование списка адресов страницы регистрации первой ожидаемой тренировки
    url_reg_week_train.append(URL_REG + str(LAST_NUMBER + 1 + i))







registration()
