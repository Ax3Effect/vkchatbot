# -*- coding: utf-8 -*-

#VK Bot by Ax3 (Nazar Kravtsov) 
# vk.com/ax3effect



'''
README
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


- Поставьте ownerID (айди самого бота)
- Поставьте controlID (ваш айди, откуда вы можете контролировать чатмодами)
- Поставьте albumID (возможность загружать картинки)

Как писать свои команды:

Там где находятся все переменные для команд, вписывайте так же вроде:
msg_blablabla = ["blablabla"]

И синтаксис самих функций всегда такой же:
    #elif msg.split(' ')[0] in msg_blablabla:
        #vk_message = "TEST \n FUNCTION"
        #msgsend(userid, vk_message, chat_id)


vk_message = сообщение, которое будет передано
msgsend - команда для отправки


По всем вопросам - https://vk.com/ax3effect
'''




# Main Modules


import vk
import time, threading
import requests
try:
    import ujson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json

import traceback
import re
import urllib.request
import io
import glob
import sys
import os
from datetime import datetime
from time import strftime
from random import randint
from configobj import ConfigObj
import random
import xml.etree.ElementTree as ET
import subprocess
from io import StringIO
# Secondary Modules
try:
    print("Initializing ReddiWrap...  ", end="")
    from ReddiWrap import ReddiWrap
    reddit = ReddiWrap()
    reddit_enable = 1
    print("[DONE]")
except ImportError:
    print("Reddit Module missing")
    reddit_enable = 0
    pass

try:
    import termcolor
    def _bold(text):
        return termcolor.colored(text, attrs=['bold'])
except ImportError:
    print("termcolor Module missing")
    def _bold(text):
        return text
    pass


try:
    print("Initializing dataset...  ", end="")
    import dataset
    database_enable = 1
    log_enable = 1
    print("[DONE]")
except ImportError:
    print("No module 'dataset'. Database statistics disabled")
    database_enable = 0
    log_enable = 0
    pass

try:
    from wand.drawing import Drawing
    from wand.image import Image
    from wand.color import Color
    imageEdit_enable = 1
except ImportError:
    imageEdit_enable = 0
    pass

try:
    import feedparser
    news_enable = 1
except ImportError:
    news_enable = 0
    pass


#### Settings
customMsg = "// бoт"
show_names = 0 # 1 or 0, disable it for better performance
blacklist = [151851224] # blacklist, VK ID's
chat_blacklist = [] # chat blacklist, VK Chat ID's
albumID = 210832058 # album for uploading photos, ID ------- SET IT UP !!!! 
ownerID = 286006014 # bot ID ------- SET IT UP !!!! 
controlID = 10399749 # admin ID ------- SET IT UP !!!!
keyWord_enable = 0
keyWord = "ч"
#database_enable = 0  #override database setting

#### Settings

#### Config files
config = ConfigObj("settings.ini")
forecastioAPI = config['forecastio']
customMsg = config['custommsg']
controlID = int(config['controlID'])
#### Config files

#### Multi-user
try:
    mainBotID = int(config['mainBotID'])
except Exception:
    mainBotID = 0

if mainBotID == 1:
    vk_access_token = config['vk_token_1']
    albumID = config['album_id_1']
elif mainBotID == 2:
    vk_access_token = config['vk_token_2']
    albumID = config['album_id_2']
else:
    vk_access_token = config['vk_token']
    albumID = config['album_id']

try:
    probability = config['probability']
except Exception:
    probability = 0






print("Initializing...")

#### Help messages
helpMessage = (" - Помощь по командам - \n"
    "✨тест \n"
    "✨привет \n"
    "✨курс \n"
    "✨погода [город] \n"
    "✨сосчитать (13 * 37) \n"
    "✨правда [ваш вопрос] \n"
    "✨статистика \n"
    "✨баш \n"
    "✨reddit [название реддита] [n, p]\n"
    "✨аудио [название трека]\n"
    "✨новости\n"
    "✨код\n"
    "✨инфа [что-либо]\n"
    "✨пошути\n"
    "✨колво"
    "\n"
    )

#### Text messages variables
msg_test = ["test", "тест", "Тест"]
msg_help = ["help", "помощь", "Помощь"]
msg_hi = ["hi", "привет", "Привет"]
msg_exchange = ["exchange", "rates", "курс", "Курс"]
msg_weather = ["weather", "погода", "Погода"]
msg_calc = ["calc", "сосчитать", "Сосчитать"]
msg_truth = ["truth", "правда", "Правда"]
msg_stats = ["stats", "статистика", "Cтатистика"]
msg_imagetest = ["image", "имага", "Имага"]
msg_publictest = ["мasd", "mdsa"]
msg_autochatmode1on = ["swe_on"]
msg_autochatmode1off = ["swe_off"]
msg_bashorg = ["bash", "баш", "Баш", "башорг"]
msg_padik = ["ghetto", "падик", "Падик"]
msg_reddittop = ["reddit", "r", "реддит", "Реддит"]
msg_img = ["time", "время", "Время"]
msg_chatmode = ["чатмод"]
msg_vkaudio = ["аудио", "audio"]
msg_blacklistadd = ["!blacklist_add"]
msg_countcheck = ["колво"]
msg_imagepack = ["пак"]
msg_shortiki = ["пошути"]
msg_owner = ["владелец"]
msg_infa = ["инфа"]
msg_restart = ["рестарт"]
msg_codelines = ["код"]
msg_news = ["новости"]
msg_changeMain = ["!bot_change"]
msg_controlexec = ["!exec"]
msg_convert = ["валюта"]
msg_changetextid = ["!add_id"]
msg_showchatid = ["!show_id"]
msg_changetexttеxt = ["!changetitle"]
msg_author = ["автор"]

#### Variables
attempt_id = 0
chat_id = 0
weather_disable = 0 
autoChatMode = 0
redditCounter = 1
connect_success = 0
global prepareTextFile
global linesList
global changetxtids
global desiredTitle
global rexec
rexec = ""
desiredTitle = "test"
prepareTextFile = 0
changetxtids = []





# VK API
vkapi = vk.API(access_token=vk_access_token)





# -------- Answer Functions -------

def emoji():
    hat = "🎩 🎩 👑 👒 💛 💙 ☁ 💡 📪 💕 ⚡ ☔ ❄ ⛄ 💭"
    hat = hat.split()
    face = "😄 😃 😀 😊 ☺ 😉 😍 😘 😚 😗 😙 😜 😝 😛 😳 😁 😔 😌 😒 😞 😣 😢 😂 😭 😪 😥 😰 😅 😓 😩 😫 😨 😱 😠 😡 😤 😖 😆 😋 😷 😎 😴 😵 😲 😟 😦 😧 😈 👿 😮 😬 😐 😕 😯 😶 😇 😏 😑 👲 👳 👮 👷 💂 👶 👦 👧 👨 👩 👴 👵 👱 👼 🐶 🐺 🐱 🐭 🐹 🐰 🐸 🐯 🐨 🐻 🐷 🐮 🐵 🐼 🐧 🐦 🐤 🐥 🐣 🐔 🐓 🙉 🙊 💀 👽 💩"
    face = face.split()
    body = "👕 👔 👚 👗 🎽 👖 👘 👙"
    body = body.split()
    hand = "🍪 📱 ☎ 📞 🎥 📷 📹 🏈 🚬 🏀 ⚽ ⚾ 🎾 🎱 🏉 ☕ 🍵 🍶 🍼 🍺 🍻 🍸 🍹 🍷 🍴 🍕 🍔 🍟 🍗 🍖 🍝 🍛 🍤 🍱 🍣 🍥 🍙 🍘 🍚 🍜 🍲 🍢 🍡 🍳 👍 👎 👌 👊 ✊ ✌ 👋 ✋ 👐 🙌 🙏 ☝ 👏 💪 "
    hand = hand.split()
    shoes = "👡 👠 👡 👟 👞 👢"
    shoes = shoes.split()

    hat = random.choice(hat)
    face = random.choice(face)
    body = random.choice(body)
    lhand = random.choice(hand)
    rhand = random.choice(hand)
    shoes = random.choice(shoes)

    finalResult1 = "   {}  \n".format(hat)
    finalResult2 = "   {}  \n".format(face)
    finalResult3 = "{}{}{}\n".format(lhand,body,rhand)
    finalResult4 = "  {}{} \n".format(shoes,shoes)
    finalResult = finalResult1 + finalResult2 + finalResult3 + finalResult4
    return finalResult

def padik():
    randomNumber = randint(40000, 700000)
    wallGet = vkapi.wall.get(domain = "pad_iks", offset = randomNumber, count = 1)
    wallPhoto2 = wallGet["items"]
    wallPhoto3 = wallPhoto2[0]["text"]
    if wallPhoto3 != "":
        vk_message = wallPhoto3
        msgsend(userid, vk_message, chat_id)


def imgText():
    # TODO
    # NOT FINISHED
    pass
    '''
    msgImgSplit = msg.split(' ')
    print(msgImgSplit)
    msgImgSplit = msgImgSplit[1]
    with Drawing() as draw:
            # does something with ``draw`` object,
            # and then...
        with Image(filename='photoR.jpg') as image:
            with Color('white') as color:
                draw.font = 'SourceSansPro-Regular.otf'
                draw.font_size = 150
                draw.fill_color = color
                draw.text(200,200, msgImgSplit)
                draw(image)
                image.save(filename='photo.jpg')
                imagetestContent = uploadImage()
                vk_message = ""
                msgsend(userid, vk_message, chat_id, imagetestContent[0]["id"])'''

def answerBaseInit():
    with open('baza1.txt') as f:
        lines = f.read().splitlines()
    words = [w.replace(' (', '') for w in lines[::2]]
    words = [w.replace('.)', '') for w in words]
    words = [w.replace(')', '') for w in words]
    words = [w.replace('?', '') for w in words]
    words = [w.replace('.', '') for w in words]
    words = [w.replace('{', '') for w in words]
    words = [w.replace('}', '') for w in words]
    words = [w.replace('[', '') for w in words]
    words = [w.replace(']', '') for w in words]
    questions = words
    answers = lines[1::2]
    global dictionary
    dictionary = dict(zip(questions, answers))

try:
    answerBaseInit()
    answerBase_enable = 1
except Exception:
    answerBase_enable = 0

def chatidcheck(chatcheck):
    if str(chatcheck)[-3:][0] == 0:
        chatcheckid = str(chatcheck)[-2:]
        #print(chatcheckid)
        return chatcheckid
    else:
        chatcheckid = str(chatcheck)[-3:]
        #print(chatcheckid)

        return chatcheckid

def downloadImage(url):
    image_name = 'photo.jpg'
    urllib.request.urlretrieve(url, image_name)


if database_enable == 1:
    db = dataset.connect('sqlite:///vkcount2.db')
    global table
    table = db['user']
    def database(vid, vname):
        checkExist = table.find_one(vid=vid)
        try:
            #print checkExist["vcount"]
            if checkExist["vcount"] or checkExist["vcount"] == 0:
                ccount = checkExist["vcount"] + 1
                #print "CCOUNT - " + str(ccount)
                table.update(dict(vid=vid, vcount=ccount), ['vid'])
        except Exception:
            print("New user " + str(vid))
            table.insert(dict(vid=vid, vname=vname, vcount=0))
        #for user in db['user']:
            #print "ID : " + str(user['vid']) 
            #print "VCOUNT : " + str(user['vcount'])

if log_enable == 1:
    db_log = dataset.connect('sqlite:///vk_log.db')
    global table_log
    table_log = db_log['user']
    def logDatabase(userid, chatid, name, msg):
        try:
            if msg == "":
                pass
            else:
                table_log.insert(dict(userid=userid, chatid=chatid, name=name, msg=msg))
        except Exception:
            traceback.print_exc()

def yandexNews():
    newsURL = "http://news.yandex.ru/index.rss"
    news = requests.get(newsURL).text
    root = ET.fromstring(news)
    
def initTextBase():
    global linesList
    with open('textFile.txt', encoding="utf-8") as f:
        linesList = f.readlines()


# Friends add function
def friendsAdd():
    getRequests = vkapi.friends.getRequests()
    for eachFriend in getRequests["items"]:
        print("Added " + str(eachFriend) + " as a friend")

        vkapi.friends.add(user_id = eachFriend)
        time.sleep(10)
    time.sleep(70)
    friendsAdd()



t = threading.Thread(target = friendsAdd)
t.start()
initTextBase()


def changeText():
    while True:
        print("checking name...")
        if changetxtids:
            for i in changetxtids:
                getChatInfo = vkapi.messages.getChat(chat_id= i)
                try:
                    chatPhoto = getChatInfo["photo_50"]
                    vkapi.messages.deleteChatPhoto(chat_id = i)
                except KeyError:
                    pass
                except Exception:
                    traceback.print_exc()
                time.sleep(2)
                try:
                    chatName = getChatInfo["title"]
                    if str(chatName) != desiredTitle:
                        vkapi.messages.editChat(chat_id = i, title=desiredTitle)
                except Exception:
                    traceback.print_exc()
        time.sleep(15)

#changeTextThread = threading.Thread(target = changeText)
#changeTextThread.start()


# ---------- Message Check Function --------

def msgcheck(msg, id=None):
    global autoChatMode
    global chat_id
    global attempt_id
    global redditCounter
    global lereddit
    attempt_id = attempt_id + 1 # VK anti-block system

    msg = str(msg)
    #logDatabase(userid, chat_id, theName, msg)
    msg = msg.lower()
    if msg.split(' ')[0] in msg_test:
        vk_message = "Вы ввели тестовую команду\n Рандом: {}".format(str(randint(2,100))) + "%."
        msgsend(userid, vk_message, chat_id)
    elif msg.split(' ')[0] in msg_help:
        msgsend(userid, helpMessage, chat_id)
    elif msg.split(' ')[0] in msg_hi:
        vk_message = "Привет!\n Напиши мне слово помощь, чтобы узнать список команд." 
        msgsend(userid, vk_message, chat_id)
    elif msg.split(' ')[0] in msg_exchange:
        kurs = requests.get("http://api.fixer.io/latest?base=USD")
        kursbid1 = kurs.json()["rates"]
        kursbid = kursbid1["RUB"]
        kurs_euro = requests.get("http://api.fixer.io/latest?base=EUR")
        kursbid1_euro = kurs_euro.json()["rates"]
        kursbid_euro = kursbid1_euro["RUB"]
        kurs_gbp = requests.get("http://api.fixer.io/latest?base=GBP")
        kursbid1_gbp = kurs_gbp.json()["rates"]
        kursbid_gbp = kursbid1_gbp["RUB"]
        vk_message = "1 Доллар = {} руб. \n 1 Евро = {} руб. \n 1 Фунт = {} руб".format(kursbid, kursbid_euro, kursbid_gbp)
        msgsend(userid, vk_message, chat_id)
    elif msg.split(' ')[0] in msg_weather:
        if weather_disable == 0:
            #print("got it!")
            msgGeoSplit = msg.split()
            msgGeoSplit = msgGeoSplit[1:]
            msgGeoString = ' '.join(msgGeoSplit)
            if msgGeoString == "":
                vk_message = "⚠ Используй:\n погода [город]"
                msgsend(userid, vk_message, chat_id)
            else:
                geocodeURL = "https://maps.googleapis.com/maps/api/geocode/json?address={}&sensor=false&language=ru".format(msgGeoString)
                geocodeRequest = requests.get(geocodeURL)
                geoResult2 = geocodeRequest.json()

                if geoResult2["status"] == "OK":
                    geoResult = geoResult2["results"]
                    geoLocation1 = geoResult[0]["geometry"]
                    geoLocation2 = geoLocation1["location"]
                    geoLat = geoLocation2["lat"]
                    geoLng = geoLocation2["lng"]
                    print("Lat: {}, Lng: {}".format(geoLat, geoLng))

                    forecastURL = "https://api.forecast.io/forecast/{}/{},{}?units=si".format(forecastioAPI, geoLat, geoLng)

                    forecastGet = requests.get(forecastURL)
                    forecastJSON = forecastGet.json()

                    forecastp1 = forecastJSON["currently"]
                    forecastp2 = forecastp1["temperature"]
                    forecastp2Summary = forecastp1["summary"]
                    forecastp2Windspeed = forecastp1["windSpeed"]
                    forecastp2Hum = forecastp1["humidity"]
                    forecastp2Pressure = forecastp1["pressure"]
                    vk_message = "Погода: {}\nLat: {}, Lng: {} \nhttps://www.google.ru/maps/@{},{},16z \n Температура воздуха: {}°C \n {} \n Скорость ветра: {}м/c \n Влажность: {}% \n Давление: {} мм. рт. ст.".format(msgGeoString, geoLat, geoLng, geoLat, geoLng, forecastp2, forecastp2Summary, forecastp2Windspeed, forecastp2Hum*100, forecastp2Pressure)
                    msgsend(userid, vk_message, chat_id)

                else:
                    vk_message = "⚠ Такой город не найден!"
                    msgsend(userid, vk_message, chat_id)

    elif msg.split(' ')[0] in msg_calc:
        msgCalc = msg.split()
        msgCalc = msgCalc[1:]
        try:
            if msgCalc[1] == "+":
                msgCalcResult = int(msgCalc[0]) + int(msgCalc[2])
                vk_message = "Результат: {}".format(msgCalcResult)
                msgsend(userid, vk_message, chat_id)
            elif msgCalc[1] == "-":
                msgCalcResult = int(msgCalc[0]) - int(msgCalc[2])
                vk_message = "Результат: {}".format(msgCalcResult)
                msgsend(userid, vk_message, chat_id)
            elif msgCalc[1] == "*":
                msgCalcResult = int(msgCalc[0]) * int(msgCalc[2])
                vk_message = "Результат: {}".format(msgCalcResult)
                msgsend(userid, vk_message, chat_id)
            elif msgCalc[1] == "/":
                msgCalcResult = int(msgCalc[0]) / int(msgCalc[2])
                vk_message = "Результат: {}".format(msgCalcResult)
                msgsend(userid, vk_message, chat_id)
            else:
                vk_message = "⚠ Неправильный ввод! Вы ввели: " + str(msg)
                msgsend(userid, vk_message, chat_id)
        except Exception:
            vk_message = "⚠ Неправильный ввод! Пример: 7 + 3, 51 / 3"
            msgsend(userid, vk_message, chat_id)
    elif msg.split(' ')[0] in msg_truth:
        pravdamsg = []
        goodmsg = ["🎱Абсолютно!", "🎱Абсолютно точно!", "🎱Верно!", "🎱Правда!", "🎱Конечно же да!", "🎱Бесспорно.", "🎱Думаю да."]
        neutralmsg = ["🎱Возможно.", "🎱Не уверен.", "🎱Лучше не рассказывать.", "🎱Весьма сомнительно."]
        badmsg = ["🎱Скорее всего нет.", "🎱Врядли.", "🎱Что-то мне подсказывает, что нет.", "🎱Конечно нет.", "🎱Перспективы не очень хорошие.", "🎱Неправда. "]
        pravdamsg = goodmsg + neutralmsg + badmsg
        pravdafinal = random.choice(pravdamsg)
        vk_message = str(pravdafinal)
        msgsend(userid, vk_message, chat_id)
    elif msg.split(' ')[0] in msg_stats:
        try:
            print("Stats get")
            userStats = table.find_one(vid=userid)
            vk_message = "Здравствуйте, {}, вы сделали {} запросов с момента включения бота.".format(theName,userStats["vcount"])
            msgsend(userid, vk_message, chat_id)
        except Exception:
            traceback.print_exc()


    elif msg.split(' ')[0] in msg_imagetest:
        try:
            imagetestContent = uploadImage()
            vk_message = ""
            msgsend(userid, vk_message, chat_id, imagetestContent[0]["id"])
        except Exception:
            traceback.print_exc()

    elif msg.split(' ')[0] in msg_imagepack:
        try:
            listt = []
            for onlyfiles in glob.glob("/Volumes/Ax3 HD/Python/archive/*.jpg"):
                listt.append(onlyfiles)
            #print(listt)
            imagetestContent = uploadImageNew(random.choice(listt))
            vk_message = ""
            msgsend(userid, vk_message, chat_id, imagetestContent[0]["id"])
            time.sleep(0.5)
        except Exception:
            #traceback.print_exc()
            vk_message = "Картинки временно недоступны"
            msgsend(userid, vk_message, chat_id)




    elif msg.split(' ')[0] in msg_publictest:
        try:
            while True:
                for attempt in range(1, 6):
                    try:
                        randomNumber = randint(1, 2000)
                        wallGet = vkapi.wall.get(domain = "funysmsaifon", offset = randomNumber, count = 1)
                        #print(wallGet)
                        wallPhoto2 = wallGet["items"]
                        wallPhoto3 = wallPhoto2[0]["attachments"]
                        wallPhoto4 = wallPhoto3[0]["photo"]
                        wallPhoto5 = wallPhoto4["photo_604"]
                        print(wallPhoto5)
                        downloadImage(str(wallPhoto5))
                        imagetestContent = uploadImage()
                        vk_message = ""
                        msgsend(userid, vk_message, chat_id, imagetestContent[0]["id"])
                    except KeyError:
                        print("No Image found, retrying")
                        traceback.print_exc()
                break
        except Exception:
            traceback.print_exc()
            pass
    elif msg.split(' ')[0] in msg_autochatmode1on:
        if int(userid) == int(controlID):
            autoChatMode = 1
            vk_message = "// Мат включен."
            msgsend(userid, vk_message, chat_id)
    elif msg.split(' ')[0] in msg_autochatmode1off:
        if int(userid) == int(controlID):
            autoChatMode = 0
            vk_message = "// Мат выключен."
            msgsend(userid, vk_message, chat_id)

    elif msg.split(' ')[0] in msg_chatmode:
        msg = msg.split()
        msg = int(msg[1])
        if int(userid) == int(controlID):
            autoChatMode = msg
            vk_message = "// Режим чата сменен на: " + str(msg)
            msgsend(userid, vk_message, chat_id)
    elif msg.split(' ')[0] in msg_vkaudio:
        msgSplit = msg.split()
        msgSplit = msgSplit[1:]
        if msgSplit != "":
            audioInfo = vkapi.audio.search(q = str(msgSplit), count = 1)
        else:
            vk_message = "Введите название песни!"
            msgsend(userid, vk_message, chat_id)
        try:
            audioInfo = audioInfo["items"][0]
            audioFetchID = "audio" + str(audioInfo["owner_id"]) + "_" + str(audioInfo["id"])
            print(audioFetchID)
            vk_message = ""
            msgsend(userid, vk_message, chat_id, None, audioFetchID)
        except IndexError:
            vk_message = "Песня не найдена!"
            msgsend(userid, vk_message, chat_id)

    elif msg.split(' ')[0] in msg_bashorg:
        bashorg_site= "http://bash.im/random"
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8'}

        req = urllib.request.Request(bashorg_site, headers=hdr)
        raw_text = urllib.request.urlopen(req).read().decode('cp1251')

        parser = re.compile(r'<div class="text">(.*?)</div>')
        quotes_iter = parser.finditer(raw_text)
        quotes_iter = list(quotes_iter)
        quote = quotes_iter[0]
        text = quote.group(1).replace('<br>', '\n').replace('&amp;', '&').replace('&quot;', '"').replace('&gt;', '>').replace('&lt;', '<')
        vk_message = text
        msgsend(userid, vk_message, chat_id)

    elif msg.split(' ')[0] in msg_padik:
        padik()

    elif msg.split(' ')[0] in msg_reddittop:
        if reddit_enable == 1:
            msgReddit = msg.split()
            msgReddit = msgReddit[1:]

            if str(msgReddit) != "":
                if msgReddit[0] == "n":
                    redditCounter = redditCounter + 1
                elif msgReddit[0] == "p":
                    redditCounter = redditCounter - 1
                else:
                    lereddit = "/r/" + msgReddit[0]
                try:
                    if msgReddit[1] == "next":
                        redditCounter = redditCounter + 1
                except Exception:
                    pass

                pics = reddit.get(lereddit)
                try:
                    submissions = pics[redditCounter]
                except Exception:
                    vk_message = "Реддит не найден."
                    msgsend(userid, vk_message, chat_id)
                    pass
                submissionsurl = submissions.url
                if str(submissionsurl).find("http://imgur.com/") == 0:
                    newlink1 = submissionsurl[17:]
                    newlink = "http://i.imgur.com/" + newlink1 + ".jpg"
                    vk_message = "▶ Позиция: " + str(redditCounter)
                    downloadImage(newlink)
                    imagetestContent = uploadImage()
                    msgsend(userid, vk_message, chat_id, imagetestContent[0]["id"])
                elif submissions.url[-4:] == ".jpg" or submissions.url[-4:] == ".png":
                    downloadImage(submissions.url)
                    imagetestContent = uploadImage()
                    vk_message = "▶ Позиция: " + str(redditCounter)
                    msgsend(userid, vk_message, chat_id, imagetestContent[0]["id"])

                elif submissions.selftext != "":
                    vk_message = "▶ Позиция: " + str(redditCounter) + "\n" + submissions.title + "\n" + submissions.selftext
                    msgsend(userid, vk_message, chat_id)
                else:
                    vk_message = "▶ Позиция: " + str(redditCounter) + "\n" + submissions.title + "\nhttp://reddit.com" + submissions.permalink
                    msgsend(userid, vk_message, chat_id)
                #vk_message = submissions
                #msgsend(userid, vk_message, chat_id)

    elif msg.split(' ')[0] in msg_img:
        if imageEdit_enable == 1:
            imgText()

    elif msg.split(' ')[0] in msg_countcheck:
        countCheck = vkapi.messages.getHistory(chat_id = chat_id, offset = 0, count = 1, rev = 0)
        vk_message = "Всего в этой конференции: " + str(countCheck["count"]) + " сообщений с момента вступления в конференцию. "
        msgsend(userid, vk_message, chat_id)

    elif msg.split(' ')[0] in msg_blacklistadd:
        if userid == ownerID:
            msgBlacklist = msg.split()
            msgBlacklist = msgReddit[1:]
            blacklist.append(msgBlacklist)




    elif msg.split(' ')[0] in msg_shortiki:
        '''shURL = "http://shortiki.com/export/api.php?format=json&type=random&amount=1"
        shJSON = requests.get(shURL)
        shJSON = shJSON.json()
        vk_message = shJSON[0]["content"]
        #print(vk_message)'''
        padik()
        #msgsend(userid, vk_message, chat_id)

    elif msg.split(' ')[0] in msg_infa:

        msgInfa = msg.split()
        msgInfa = msgInfa[1:]
        msgInfa = ' '.join(msgInfa)
        vk_message = "Инфа, что {} - {}%. ".format(msgInfa, str(randint(2,100)))
        msgsend(userid, vk_message, chat_id)

    elif msg.split(' ')[0] in msg_restart:
        if int(userid) == controlID:
            vk_message = "Ухожу в рестарт!"
            msgsend(userid, vk_message, chat_id)
            python = sys.executable
            os.execl(python, python, * sys.argv)
    elif msg.split(' ')[0] in msg_codelines:
        num_lines = sum(1 for line in open('main.py'))
        vk_message = "Сейчас в коде {} строк.".format(str(num_lines))
        msgsend(userid, vk_message, chat_id)

    elif msg.split(' ')[0] in msg_news:
        news_enable = 1
        if news_enable == 1:
            news_url = "http://news.yandex.ru/index.rss"
            feed = feedparser.parse(news_url.decode("utf-8"))
            summaryHeadlines = " "
            for i in range(0, 5):
                summaryHeadlines = summaryHeadlines + feed["items"][i]["title"] + "\n⚡"
                summaryHeadlines = summaryHeadlines + feed["items"][i]["description"] + "\n\n"
            #print(summaryHeadlines)
            vk_message = summaryHeadlines
            msgsend(userid, vk_message, chat_id)

    elif msg.split(' ')[0] in msg_showchatid:
        vk_message = "Chat ID: " + str(chat_id)
        msgsend(userid, vk_message, chat_id)

    elif msg.split(' ')[0] in msg_changetextid:
        if int(userid) == controlID:
            msgtextid = msg.split()
            msgtexid = msgtextid[1]
            changetxtids.append(int(msgtexid))
            vk_message = "Успешно изменено на " + str(msgtexid) 
            msgsend(userid, vk_message, chat_id)

    elif msg.split(' ')[0] in msg_changetexttеxt:
        if int(userid) == controlID:
            msgtextid = msg.split()
            #msgtextid = msgtextid[1:]
            msgtexid = " "
            msgtexid = msgtexid.join(msgtextid[1:])
            global desiredTitle
            desiredTitle = str(msgtexid)
            vk_message = "Успешно изменено на " + str(msgtexid) 
            msgsend(userid, vk_message, chat_id)

    elif msg.split(' ')[0] in msg_author:
        vk_message = "Автор бота: Назар Кравцов (vk.com/ax3effect) :)"
        msgsend(userid, vk_message, chat_id)
    elif msg.split(' ')[0] in msg_convert:
        #nothing
        pass
    elif msg.split(' ')[0] in msg_changeMain:
        getMsgSplit = msg.split(' ')[1]
        if int(getMsgSplit) == 1 or int(getMsgSplit) == 2:
            config['mainBotID'] = getMsgSplit
            config.write()
            vk_message = "Бот сменился на аккаунт #{} \n Ухожу в рестарт!".format(getMsgSplit)
            msgsend(userid, vk_message, chat_id)
            python = sys.executable
            os.execl(python, python, * sys.argv)



            

    #TEMPLATE FUNCTION
    #elif msg.split(' ')[0] in msg_whatever:
        #vk_message = "TEST \n FUNCTION"
        #msgsend(userid, vk_message, chat_id)


    else:
        if autoChatMode == 1:
            #Huificator
            try:
                huifURL = "http://huifikator.ru/api.php?text=" + str(msg)
                huifGet = requests.get(huifURL)
                huifGet = huifGet.text
                vk_message = huifGet
                msgsend(userid, vk_message, chat_id)
            except Exception:
                traceback.print_exc()
                pass
        elif autoChatMode == 2:
            #Padik
            padik()
        elif autoChatMode == 3:
            #Answer Base
            stopAnswering = 0
            if answerBase_enable == 1:
                msg = msg.replace('?', '')
                for q, a in dictionary.items():
                    if stopAnswering == 0:
                        if q in msg:
                            print(a)
                            vk_message = a
                            msgsend(userid, vk_message, chat_id)
                            stopAnswering = 1
        elif autoChatMode == 4:
            # Wipe
            vk_message = ""
            for gfg in range(1, 500):
                vk_message = vk_message + ".\n"
            vk_message = vk_message + "."
            msgsend(userid, vk_message, chat_id)

        elif autoChatMode == 5:
            # Specific message
            vk_message = "bump " + str(attempt_id)
            msgsend(userid, vk_message, chat_id)
        elif autoChatMode == 6:
            # Emoji
            vk_message = emoji()
            msgsend(userid, vk_message, chat_id)
        elif autoChatMode == 7:
            # nothing here
            pass
        elif autoChatMode == 8:
            try:
                while True:
                    try:
                        # govnokod
                        randomNumber = randint(1, 90)
                        wallGet = vkapi.wall.get(domain = "curvedmirror", offset = randomNumber, count = 1)
                        print(wallGet)
                        wallPhoto2 = wallGet["items"]
                        wallPhoto3 = wallPhoto2[0]["attachments"]
                        wallPhoto4 = wallPhoto3[0]["photo"]
                        wallPhoto5 = wallPhoto4["photo_604"]
                        print(wallPhoto5)
                        downloadImage(str(wallPhoto5))
                        imagetestContent = uploadImage()
                        vk_message = ""
                        msgsend(userid, vk_message, chat_id, imagetestContent[0]["id"])
                    except KeyError:
                        print("No Image found, retrying")
                        traceback.print_exc()
                        continue
                    break
            except Exception:
                #traceback.print_exc()
                pass

        elif autoChatMode == 9:
            # nothing here
            '''
            randomInt = randint(1, 825)
            randomMessage = table_log.find_one(id=randomInt)
            vk_message = randomMessage["msg"]
            msgsend(userid, vk_message, chat_id)'''
            pass

        elif autoChatMode == 10:
            # nothing here
            pass

        elif autoChatMode == 11:

            randomImageChance = random.random()
            if randomImageChance < float(probability):
                chosenMsg = ""
                chosenMsg = random.choice(linesList)
                vk_message = str(chosenMsg)
                msgsend(userid, vk_message, chat_id, None, None, id)


def uploadImage():
    uploadURL = vkapi.photos.getUploadServer(album_id = albumID)
    uploadRequest = requests.post(uploadURL["upload_url"], files={"file1": open('photo.jpg', 'rb')})
    uploadContent = uploadRequest.json()    
    uploadSave = vkapi.photos.save(album_id = albumID, server=uploadContent["server"], photos_list=uploadContent["photos_list"], hash=uploadContent["hash"])
    return uploadSave

def uploadImageNew(path):
    uploadURL = vkapi.photos.getUploadServer(album_id = albumID)
    uploadRequest = requests.post(uploadURL["upload_url"], files={"file1": open(path, 'rb')})
    uploadContent = uploadRequest.json()    
    uploadSave = vkapi.photos.save(album_id = albumID, server=uploadContent["server"], photos_list=uploadContent["photos_list"], hash=uploadContent["hash"])
    print("Uploading success")
    return uploadSave



def msgsend(userid, message, chatid, photoID=None, audioID=None, forwardID=None):
    try:
        atest = result2[7]["from"]
        try:
            if int(userid) in blacklist:
                pass
                #message = "You are banned, Mr." + str(lastName) + "."
                #vkapi.messages.send(chat_id = chat_id, message = message)
            elif int(chatid) in chat_blacklist:
                pass
            else:
                if photoID != None:
                    message = message + "\n\n" + customMsg
                    readyphotoID = "photo" + str(ownerID) + "_" + str(photoID)
                    print(readyphotoID)
                    if forwardID == None:
                        vkapi.messages.send(chat_id = chat_id, message = message, attachment=readyphotoID)
                    else: 
                        vkapi.messages.send(chat_id = chat_id, message = message, attachment=readyphotoID, forward_messages=forwardID)

                elif audioID != None:
                    message = message + customMsg
                    vkapi.messages.send(chat_id = chat_id, message = message, attachment=audioID)
                else:
                    if message != "":
                        message = message + "\n\n" + customMsg
                        #message = message + "\n\n" + customMsg + str(attempt_id)
                        if forwardID == None:
                            vkapi.messages.send(chat_id = chat_id, message = message)
                        else:
                            vkapi.messages.send(chat_id = chat_id, message = message, forward_messages=forwardID)
        except vk.api.VkAPIMethodError as vkerror:
            if str(vkerror).find("14. Captcha") == 0:
                print("[ERROR] Captcha needed! Cooling down...")
                time.sleep(5)
                pass
    except KeyError:
        try:            
            if int(userid) in blacklist:
                pass
            if photoID != None:
                message = message + "\n\n" + customMsg + str(attempt_id)
                readyphotoID = "photo" + str(ownerID) + "_" + str(photoID)
                vkapi.messages.send(message = message, user_id = userid, attachment=readyphotoID)
            elif audioID != None:
                message = message + customMsg
                vkapi.messages.send(message = message, user_id = userid, attachment=audioID)
            else:
                message = message + "\n\n" + customMsg
                #message = message + "\n\n" + customMsg + str(attempt_id)
                vkapi.messages.send(message = message, user_id = userid)
        except Exception:
            pass
        pass


print("Connected!")

asd = vkapi.messages.getLongPollServer(use_ssl = 0) # getting all info for connection
ts = asd["ts"] # ts parameter for first msg getting

# Main function
while True:
    try:
        urlstring = "http://" + str(asd["server"]) + "?act=a_check&key=" + str(asd["key"]) + "&ts=" + str(ts) + "&wait=25&mode=2"
        response = requests.get(urlstring).json()
        print(response)
        ts = response["ts"] # ts for next request
        response = response["updates"][0] 
        result2 = response
        if connect_success == 0:
            print("Success!")
            connect_success = 1
    except Exception:
        traceback.print_exc()
        pass
    try:
        
        if result2[0] == 4: # message received code
            try:
                userid = result2[7]["from"] # chat message or user message
            except Exception:
                userid = result2[3]
                pass


            if userid == ownerID: #duplicate
                pass
            else:
                #if show_names == 1:
                try:
                    database_enable = 0
                    if database_enable == 1:
                        checkExist = table.find_one(vid=userid)
                        theName = checkExist["vname"]
                    '''else:
                        profiles = vkapi.users.get(user_id=userid)
                        firstName = profiles[0]['first_name']
                        lastName = profiles[0]['last_name']
                        theName = profiles[0]['first_name'] + " " + profiles[0]['last_name']
                        '''
                    #print "-------" + theName
                    if database_enable == 1:
                        database(userid, theName)
                except Exception:
                    traceback.print_exc()
                    print("--- User get failed!")
                    pass
                if str(result2[3])[:3] == "200":
                    chat_id = chatidcheck(result2[3])
                #print(str(_bold(theName)) + ": " + str(result2[6]))

                if keyWord_enable == 1:
                    mesSplit = str(result2[6]).split()
                    mesSplit2 = mesSplit[0].lower()
                    print(mesSplit2)
                    if str(mesSplit2) == str(keyWord):
                        msgToSend = ' '.join(mesSplit[1:])
                        msgcheck(msgToSend)
                else:
                    msgcheck(str(result2[6]), str(result2[1]))
    except vk.api.VkAPIMethodError:
        traceback.print_exc()
        vk_message = "⚠ Загрузка не удалась."
        msgsend(userid, vk_message, chat_id)
    except Exception:
        traceback.print_exc()
        pass