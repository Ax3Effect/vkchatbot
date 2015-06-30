python-vkbot
============

Это новая версия бота, многое будет меняться, будьте осторожны

Как установить:

Обязательные файлы, которые вам нужно взять:
* main.py
* settings_example.ini
* plugins/base_functions.ini

Для тех, кто в первый раз ставит бота:

Python 3

Необходимые модули:
- pip3 install vk
- pip3 install requests


- Сделайте файл "settings.ini" в корне рядом с скриптом, и в этом файле напишите типа:
vk_token = ВАШ ТОКЕН

К примеру: 
vk_token = 53i1r4mfhi65n7
и т.д.

Пример есть в файле "settings_example.ini", заполняйте его и переименовывайте в "settings.ini"

КАК ПОЛУЧИТЬ ТОКЕН:

Заходим сюда https://vk.com/dev
Вписываем название приложения и кликаем на "Standalone-приложение"
После этого, заходите в редактирование приложения - Настройки, и копируем ID приложения куда-нибудь
Дальше, берёте этот линк:
https://oauth.vk.com/oauth/authorize?client_id=[ ВАШ ID ПРИЛОЖЕНИЯ ]&scope=notify,friends,photos,audio,video,docs,notes,pages,status,wall,groups,messages,notifications,stats,offline&redirect_uri=http://vk.com&display=page&v=5.26&response_type=token
И вписываем ID приложения в ?client_id=
После этого, выскакивает окошко вк, нажимаем "Разрешить"
И самое главное - после этого, кликаем на строку адреса и выписываем всё что есть на "access_token" и перед &expires_in
Теперь у нас есть токен.



Как писать свои команды:

Заходите в папку /plugins/base_functions.py и пишите @respond_to("прикол") перед функцией, которая будет вызываться!

@respond_to("прикол")
def prikol(msg):
    return "123123"

Потом обязательно ищем "ALL_FUNCTIONS" и вписываем ИМЯ ФУНКЦИИ туда! Иначе не будет работать.


По всем вопросам - https://vk.com/ax3effect


============




VK Chat bot written on Python.

You need:

* Python 3 (doesn't work on Python 2)
* vk (pip install vk)
* requests (pip install requests)
* configobj (pip install configobj)

Secondary modules (not necessary):
* termcolor - for making names bold in terminal (pip install termcolor)
* dataset - for logging message count (pip install dataset)
* ReddiWrap - for reddit things - download ReddiWrap.py from https://github.com/derv82/reddiwrap/ and put it in the root folder
* Wand - http://docs.wand-py.org/en/0.3.8/

Also you need to provide access_token (you can find out more at https://vk.com/dev/auth_mobile )
And you need to provide "settings.ini" file with "vk_token" on it, like:
vk_token = "123asd".
You may also add Forecast.io API key:
forecastio = "321dsa"

Don't forget to customize your IDs in the script.
