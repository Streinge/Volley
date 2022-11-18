import requests
import fake_useragent
# адрес сайта
LINK = 'http://sportforus.ru/'
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
Responce_second = session_second.post(LINK, data=data_second, headers=header_second).text
# получение длины контента страницы аккаунта
length_account_second = session_second.get(URL_account_second, stream=True).headers['Content-Length']
print('Аккаунт Полины', length_account_second)
for i in range(7):
    length_account_second = session_second.get(URL_account_second, stream=True).headers['Content-Length']
    print('Аккаунт Полины', i, length_account_second)
    i+=1