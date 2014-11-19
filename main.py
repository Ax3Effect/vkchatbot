# -*- coding: utf-8 -*-

# VK Bot by Ax3 (Nazar Kravtsov) 
# vk.com/ax3effect

# --------------- EXPERIMENTAL -------------

#https://oauth.vk.com/authorize?client_id=4379184&scope=notify,friends,photos,audio,video,docs,notes,pages,status,wall,groups,messages,notifications,stats,offline,nohttps&redirect_uri=http://vk.com&display=page&v=5.26&%20response_type=token

# Main Modules
import vk
import time, threading
import requests
import simplejson as json
import ast
import traceback
import re
import urllib.request
import io
import glob
from datetime import datetime
from time import strftime
from random import randint
from configobj import ConfigObj
import random
# Secondary Modules
try:
    from ReddiWrap import ReddiWrap
    reddit = ReddiWrap()
    reddit_enable = 1
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
    import dataset
    database_enable = 1
except ImportError:
    print("No module 'dataset'. Database statistics disabled")
    database_enable = 0
    pass

try:
    from wand.drawing import Drawing
    from wand.image import Image
    from wand.color import Color
    imageEdit_enable = 1
except ImportError:
    imageEdit_enable = 0
    pass



#### Settings
customMsg = ""
show_names = 0 # 1 or 0, disable it for better performance
blacklist = [1,2,3,4] # blacklist, VK ID's
chat_blacklist = [81] # chat blacklist, VK Chat ID's
albumID = 206225561 # album for uploading photos, ID
ownerID = 277044695 # owner ID
controlID = 10399749 # admin ID
#database_enable = 0  #override database setting

#### Settings

#### Config files
config = ConfigObj("settings.ini")
vk_access_token = config['vk_token']
forecastioAPI = config['forecastio']
#### Config files

print("Initializing...")

#### Help messages
helpMessage = (" - Помощь по командам - \n"
    "тест \n"
    "привет \n"
    "курс \n"
    "погода [город] \n"
    "сосчитать (13 * 37) \n"
    "правда [ваш вопрос] \n"
    "статистика \n"
    "баш \n"
    "падик \n"
    "reddit\n"
    "время\n"
    "аудио\n"
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
msg_publictest = ["мемы", "memes"]
msg_autochatmode1on = ["swear_on", "мат_вкл"]
msg_autochatmode1off = ["swear_off", "мат_выкл"]
msg_bashorg = ["bash", "баш", "Баш", "башорг"]
msg_padik = ["ghetto", "падик", "Падик"]
msg_reddittop = ["reddit", "r", "реддит", "Реддит"]
msg_img = ["time", "время", "Время"]
msg_chatmode = ["чатмод"]
msg_vkaudio = ["аудио", "audio"]
msg_blacklistadd = ["!blacklist_add"]
msg_countcheck = ["колво"]
msg_imagepack = ["пак"]

#### Variables
attempt_id = 0
chat_id = 0
weather_disable = 0 
autoChatMode = 0
redditCounter = 1
connect_success = 0






# VK API
vkapi = vk.API(access_token=vk_access_token)
asd = vkapi.messages.getLongPollServer(use_ssl = 0)




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
                msgsend(userid, vk_message, chat_id, imagetestContent[0]["id"])

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
    chatcheckid = str(chatcheck)[-2:]
    return chatcheckid

def downloadImage(url):
    image_name = 'photo.jpg'
    urllib.request.urlretrieve(url, image_name)


if database_enable == 1:
    def database(vid, vname):
        db = dataset.connect('sqlite:///vkcount2.db')
        global table
        table = db['user']
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



# Friends add function
def friendsAdd():
    getRequests = vkapi.friends.getRequests()
    for eachFriend in getRequests["items"]:
        print("Added " + str(eachFriend) + " as a friend")
        vkapi.friends.add(user_id = eachFriend)
    time.sleep(70)



t = threading.Thread(target = friendsAdd)
t.start()




   





# ---------- Message Check Function --------

def msgcheck(msg):
    global autoChatMode
    global chat_id
    global attempt_id
    global redditCounter
    global lereddit
    attempt_id = attempt_id + 1 # VK anti-block system
    msg = str(msg)
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
                print(msgGeoString)
                geocodeURL = "https://maps.googleapis.com/maps/api/geocode/json?address={}&sensor=false&language=ru".format(msgGeoString)
                print(geocodeURL)
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
        except Exception:
            traceback.print_exc()




    elif msg.split(' ')[0] in msg_publictest:
        try:
            while True:
                try:
                    randomNumber = randint(1, 2000)
                    wallGet = vkapi.wall.get(domain = "funysmsaifon", offset = randomNumber, count = 1)
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
        audioInfo = vkapi.audio.search(q = str(msgSplit), count = 1)
        audioInfo = audioInfo["items"][0]
        audioFetchID = "audio" + str(audioInfo["owner_id"]) + "_" + str(audioInfo["id"])
        print(audioFetchID)
        vk_message = ""
        msgsend(userid, vk_message, chat_id, None, audioFetchID)

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
                print(submissions.url)
                print(submissions.selftext)
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
            pass

 
    else:
        if autoChatMode == 1:
            #Huificator
            try:
                huifURL = "http://huifikator.ru/api.php?text=" + str(msg)
                huifGet = requests.get(huifURL)
                huifGet = huifGet.text
                print(huifGet)
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
            if answerBase_enable == 1:
                msg = msg.replace('?', '')
                for q, a in dictionary.items():
                    if q in msg:
                        print(a)
                        vk_message = a
                        msgsend(userid, vk_message, chat_id)
        elif autoChatMode == 4:
            #Wipe
            vk_message = "\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n."
            msgsend(userid, vk_message, chat_id)

        elif autoChatMode == 5:
            #Specific message
            vk_message = "asdasd"
            msgsend(userid, vk_message, chat_id)
        elif autoChatMode == 6:
            #Emoji
            vk_message = emoji()
            msgsend(userid, vk_message, chat_id)


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



def msgsend(userid, message, chatid, photoID=None, audioID=None):
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
                    vkapi.messages.send(chat_id = chat_id, message = message, attachment=readyphotoID)

                if audioID != None:
                    message = message + customMsg
                    vkapi.messages.send(chat_id = chat_id, message = message, attachment=audioID)
                else:
                    if message != "":
                        message = message + "\n\n" + customMsg
                        #message = message + "\n\n" + customMsg + str(attempt_id)
                        vkapi.messages.send(chat_id = chat_id, message = message)
        except Exception:
            #traceback.print_exc()
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


while True:
    try:
        asd = vkapi.messages.getLongPollServer(use_ssl = 0)
        urlstring = "http://" + str(asd["server"]) + "?act=a_check&key=" + str(asd["key"]) + "&ts=" + str(asd["ts"]) + "&wait=25&mode=2"
        response = requests.get(urlstring).json()
        response = response["updates"][0]
        result2 = response
        if connect_success == 0:
            print("Success!")
            connect_success = 1
    except Exception:
        #traceback.print_exc()
        pass
    try:
        if result2[0] == 4:
            try:
                userid = result2[7]["from"]
            except Exception:
                userid = result2[3]
                pass
            #if show_names == 1:
            try:
                profiles = vkapi.users.get(user_id=userid)
                firstName = profiles[0]['first_name']
                lastName = profiles[0]['last_name']
                theName = profiles[0]['first_name'] + " " + profiles[0]['last_name']
                #print "-------" + theName
                if database_enable == 1:
                    database(userid, theName)
            except Exception:
                print("--- User get failed!")
                pass
            if str(result2[3])[:3] == "200":
                chat_id = chatidcheck(result2[3])
            print(str(_bold(theName)) + ": " + str(result2[6]))
            msgcheck(str(result2[6]))
    except vk.api.VkAPIMethodError:
        traceback.print_exc()
        vk_message = "⚠ Загрузка фото не удалась."
        msgsend(userid, vk_message, chat_id)
    except Exception:
        traceback.print_exc()
        ## ONLY DEBUG
        #vk_message = traceback.print_exc()
        #msgsend(userid, vk_message, chat_id)
        pass