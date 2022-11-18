import requests
import fake_useragent
from threading import Thread
# адрес сайта
LINK = 'http://sportforus.ru/'

# адрес страницы аккаунта
URL_account = 'http://sportforus.ru/user/Олеег/'

# функция второго подключения
def second_connection():
    URL_account_second = 'http://sportforus.ru/user/Полина Махнёва/'
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
    print('running Polina')
    # передача данных для авторизации
    session_second.post(LINK, data=data_second, headers=header_second)
    # получение длины контента страницы аккаунта
    length_account_second = session_second.get(URL_account_second, stream=True).headers['Content-Length']
    print('Аккаунт Полины', length_account_second)
    for i in range(7):
        length_account_second = session_second.get(URL_account_second, stream=True).headers['Content-Length']
        print('Аккаунт Полины', i, length_account_second)
        i+=1
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

# создание сессии при подключении к сайту
session = requests.Session()
print('running')
# передача данных для авторизации
session.post(LINK, data=data, headers=header)

# получение длины контента страницы аккаунта
length_account = session.get(URL_account, stream=True).headers['Content-Length']
print(length_account)
# запуск потока второга подключения
th3 = Thread(target=second_connection)
th3.start()

for i in range(7):
    length_account = session.get(URL_account, stream=True).headers['Content-Length']
    print(i, length_account)
    i+=1
