# -*- coding: utf-8 -*-
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
session = requests.Session()
# передача данных для авторизации
session.post(LINK, data=data, headers=header).headers
# адрес первой ожидаемой тренировки
url_new_train = URL_TRAINING + str(LAST_NUMBER + 1)
# адрес страницы регистрации первой ожидаемой тренировки
url_reg_new_train = URL_REG + str(LAST_NUMBER + 1)
# регистрация на первой ожидаемой тренировке 
session.get(url_reg_new_train, headers=header)
length_new_train = session.get(url_new_train, stream=True).headers['Content-Length']
"""if int(new_length) - FAKE_LENGTH > 100:
    for i in range(7):
        print(new_URL)
        session.get(new_URL, headers=header)
        new_URL = URL + str(LAST_NUMBER + i + 2)
        time.sleep(5)
print('OK')"""
print(int(new_length))
