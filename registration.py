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
# последний номер документа с тренировкой
LAST_NUMBER = 3715
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
# задержка по времени между опросами об изменениях страницы с тренировками
DELAY_LIST = 30
# функция регистрации на тренировках
def registration():
    for j in range(NUMBER_TRAINING):
        while True:
            time.sleep(DELAY_REG)
            # получение длины ожидаемой тренировки
            length_new_train = session.get(url_week_train[j], stream=True).headers['Content-Length']
            # проверка условия существования тренировки.
            if int(length_new_train) - FAKE_LENGTH > 100:
                print(int(length_new_train) - FAKE_LENGTH > 100)
                # регистрация на первой ожидаемой тренировке 
                session.get(url_reg_week_train[j], headers=header)
                print('Регистрация на:', url_reg_week_train[j])
                break
            else:
                print(int(length_new_train) - FAKE_LENGTH > 100)
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
