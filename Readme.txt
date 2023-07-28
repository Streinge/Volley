Необходимо установить Ubuntu 20.04 или новее, потому что в ниже версиях pip3 и sms api ru уже не поддерживает
а поменять версию Python это танцы с бубном, я попробовал 3 способа и не один не сработал
Запустим обновление базы данных пакетов Ubuntu командой apt-get update
Сделать обновление всех пакетов sudo apt-get upgrade
установка pip и обновление sudo apt install python3-pip, а потом pip3 install --user --upgrade pip
Установка Git sudo apt install git
Зайти в папку проекта и создать клон репозитария git clone https://github.com/Streinge/Volley.git
если потребуется добавить какой-то каталог в переменную PATH,то пишем название папки с двоеточием перед названием
export PATH=$PATH:/root/.local/bin
проверяем что записалось нормально командой echo $PATH
после установки pip проверяем какие службы надо переустанавливать с помощью утилиты needrestart
модуль "requests" устанавливать не надо, он уже есть в комплекте
установка модуля "fake_useragent" pip3 install fake-useragent
Если потребуется обновление модуля "fake_useragent" pip3 install --upgrade fake-useragent
установка модуля "telegram.ext" pip3 install python-telegram-bot
установка модуля "smsru_api" pip3 install smsru-api
установка модуля "decouple" pip3 install python-decouple
установка модуля "time" не требуется