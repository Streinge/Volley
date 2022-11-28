import requests
import fake_useragent

# адрес сайта
LINK = 'http://sportforus.ru/'
# Основной логин
NAME_MAIN = 'Ludmila'
# Пароль к основному логину
PASSWORD_MAIN = 'sokol15'
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


# функция получения Content-Lenght любой страницы
def length_page(url_page):
    return int(session.get(url_page, stream=True).headers['Content-Length'])


# создание сессии при подключении к сайту
session = requests.Session()
print('running')
# передача данных для авторизации
session.post(LINK, data=data, headers=header)

print(55555555 + length_page('http://sportforus.ru/wv/training/list'))
