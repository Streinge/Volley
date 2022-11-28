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
# Второй логин
NAME_SECOND = 'Олеег'
PASSWORD_SECOND = 'a5k69mf223y'
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


# функция получения Content-Lenght любой страницы
def length_page(url_page):
    return int(session.get(url_page, stream=True).headers['Content-Length'])


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


# функция регистрации на сайте
def registration():
    # регистрация на первой ожидаемой тренировке
    session.get(url_reg_week_train[0], headers=header)
    print('Регистрация на:', url_reg_week_train[0])
    second_connection(url_reg_week_train[0])
    for j in range(NUMBER_TRAINING - 1):
        # проверка наличия следующих тренировок кроме первой
        if checking_training(url_week_train[j + 1], triggering_status):
            session.get(url_reg_week_train[j + 1], headers=header)
            print('Регистрация на:', url_reg_week_train[j + 1])
            second_connection(url_reg_week_train[j + 1])
            continue
    print('Регистрация завершена')


user = fake_useragent.UserAgent().random

header = {
      'user-agent': user
}


data = {
     'login_name': NAME_MAIN.encode('cp1251'),
     'login_password': PASSWORD_MAIN,
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
    url_week_train.append(URL_TRAINING + str(last_number + 1 + i))
    # формирование списка адресов страницы регистрации первой ожидаемой
    # тренировки
    url_reg_week_train.append(URL_REG + str(last_number + 1 + i))

triggering_status = True
registration()
