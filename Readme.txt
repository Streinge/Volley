установка pip и обновление sudo apt install python3-pip, а потом pip3 install --user --upgrade pip
если потребуется добавить какой-то каталог в переменную PATH,то пишем название папки с двоеточием перед названием
export PATH=$PATH:/root/.local/bin
проверяем что записалось нормально командой echo $PATH
после установки pip проверяем какие службы надо переустанавливать с помощью утилиты needrestart
Если потребуется обновление модуля "fake_useragent" pip install --upgrade fake-useragent