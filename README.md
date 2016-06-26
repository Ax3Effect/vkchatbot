python-vkchatbot - Чат бот для ВКонтакте
============

README
Для тех, кто в первый раз ставит бота:
Python 2/3

Необходимые модули:
- pip install vk
- pip install requests
- pip install requests-futures
- pip install sqlalchemy
- pip install dogpile.cache


Гайд
===


Отредактируйте файл "settings.ini" в корне рядом с скриптом, и в этом файле вставьте ваш токен:
vk_token = ВАШ ТОКЕН
К примеру: 
vk_token = 53i1r4mfhi65n7
и т.д.

КАК ПОЛУЧИТЬ ТОКЕН:
=
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
=

В конце bot.py уже есть несколько примеров для команд. Из "словаря" data, который отсылается команде, есть переменные:

message - сам текст сообщения

user_id - тот, кто отправил сообщение

chat_id - если есть, если нету то None

timestamp - unix таймстамп

db - связь с базой данной ИМЕННО ЭТОГО КОНКРЕТНОГО ПОЛЬЗОВАТЕЛЯ

dbsession - главная сессия базы данных



Для добавления команды нужно перед функцией добавить декоратор. Есть три типа декораторов:

@msg.add('test') - функция исполняется когда прислали сообщение с текстом "test"

@msg.add_user_id('1') - функция исполняется когда прислали сообщение от пользователя под айди 1

@msg.add_chat_id('123') - функция исполняется когда прислали сообщение в конференции под айди 123

Соответственно приоритет таков - сначала текст, потом юзер айди, потом чат айди

Так же есть функция, которая будет исполняться каждый раз, когда бот включается - msg.init_function()

В конце функции, обязательно нужно отправить обратно своё сообщение. Если вы хотите просто отправить сообщение назад, пишите - return "блаблабла", если же вы хотите добавить что-то кроме текста, используйте словарь (есть пример в конце бота)

По всем вопросам - https://vk.com/ax3effect


===


VK Chat bot written on Python (Rewritten).

Requirements:

* vk (pip install vk)
* requests (pip install requests)
* sqlalchemy (pip install sqlalchemy)
* dogpile.cache (pip install dogpile.cache)
* requests-futures (pip install requests-futures)

Also you need to provide access_token (you can find out more at https://vk.com/dev/auth_mobile )
And you need to provide "settings.ini" file with "vk_token" on it, like:
vk_token = "123asd".

Don't forget to customize your IDs in the script.
