# -*- coding: utf-8 -*-
import logging
import time
import requests
import fake_useragent
logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")

session = requests.Session()

link = 'http://sportforus.ru/'
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
Responce = session.post(link, data=data, headers=header).text
# session.get('http://sportforus.ru/wv/training/reg/3700', headers=header)
""" URL = 'http://sportforus.ru/wv/training/reg/'
LAST_NUMBER = 3701
FAKE_LENGTH = 9278
FACT_LENGTH = 12781
new_URL = URL + str(LAST_NUMBER + 1)
print('Введите')
new_length = input()"""
new_length = session.get('http://sportforus.ru/wv/training/3704', stream=True).headers['Content-Length']
"""if int(new_length) - FAKE_LENGTH > 100:
    for i in range(7):
        print(new_URL)
        session.get(new_URL, headers=header)
        new_URL = URL + str(LAST_NUMBER + i + 2)
        time.sleep(5)
print('OK')"""
print(int(new_length))
