# -*- coding: utf-8 -*-

# VK Bot by Ax3 (Nazar Kravtsov) 
# vk.com/ax3effect

# Main Modules
import vk
import time, threading
import requests
import json
import ast
import traceback
import random

try:
    import dataset
    database_enable = 1
except ImportError:
    print("No module 'dataset'. Database statistics disabled")
    database_enable = 0
from datetime import datetime
from random import randint
from configobj import ConfigObj

#### Settings
customMsg = "\n // vk.com/ax3bot ID: "
show_names = 0 # 1 or 0, disable it for better performance
blacklist = [1,2,3] # blacklist, VK ID's
albumID = 203267618
ownerID = 10399749
#database_enable = 0  #override database setting

#### Settings

#### Config files
config = ConfigObj("settings.ini")
vk_access_token = config['vk_token']
geocodingAPI = config['google_geocoding']
forecastioAPI = config['forecastio']
#### Config files

print("Initializing...")

#### Help messages
helpMessage = (" - Помощь - \n"
    "test \n"
    "привет \n"
    "курс \n"
    "погода (ГОРОД) \n"
    "сосчитать (13 * 37) \n"
    "правда (что-то) \n"
    "статистика \n"
    )

#### Text messages variables
msg_test = ["test", "тест"]
msg_help = ["help", "помощь"]
msg_hi = ["hi", "привет"]
msg_exchange = ["курс", "exchange", "rates"]
msg_weather = ["weather", "погода", "Погода"]
msg_calc = ["calc", "сосчитать", "сч"]
msg_truth = ["truth", "правда", "Правда"]
msg_stats = ["stats", "статистика"]
msg_imagetest = ["image", "имага"]



attempt_id = 0
chat_id = 0
weather_disable = 0 

connect_success = 0

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





vkapi = vk.API(access_token=vk_access_token)
asd = vkapi.messages.getLongPollServer(use_ssl = 0)

def chatidcheck(chatcheck):
	chatcheckid = str(chatcheck)[-2:]
	return chatcheckid

def msgcheck(msg):
    global chat_id
    global attempt_id
    attempt_id = attempt_id + 1 # VK anti-block system
    msg = str(msg)
    if msg in msg_test:
        vk_message = "Рандом: {}".format(str(randint(2,100))) + "%."
        msgsend(userid, vk_message, chat_id)
    elif msg in msg_help:
        msgsend(userid, helpMessage, chat_id)
    elif msg in msg_hi:
        vk_message = "Привет!" 
        msgsend(userid, vk_message, chat_id)
    elif msg in msg_exchange:
        kurs = requests.get("http://api.fixer.io/latest?base=USD")
        print(kurs.json())
        kursbid1 = kurs.json()["rates"]
        kursbid = kursbid1["GBP"]
        vk_message = "1 dollar = {} pounds".format(kursbid)
        msgsend(userid, vk_message, chat_id)
    elif msg in msg_weather:
        if weather_disable == 0:
            #print("got it!")
            msgGeoSplit = msg.split()
            msgGeoSplit = msgGeoSplit[1:]
            msgGeoString = ' '.join(msgGeoSplit)
            if msgGeoString == "":
                vk_message = "Описание:\n погода (город)"
                msgsend(userid, vk_message, chat_id)
            else:
                print(msgGeoString)
                geocodeURL = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(msgGeoString, geocodingAPI)
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
                    #print forecastURL
                    forecastGet = requests.get(forecastURL)
                    forecastJSON = forecastGet.json()
                    #print forecastJSON
                    forecastp1 = forecastJSON["currently"]
                    forecastp2 = forecastp1["temperature"]
                    forecastp2Summary = forecastp1["summary"]
                    forecastp2Windspeed = forecastp1["windSpeed"]
                    forecastp2Hum = forecastp1["humidity"]
                    forecastp2Pressure = forecastp1["pressure"]
                    vk_message = "Погода: {}\nLat: {}, Lng: {} \nhttp://maps.google.co.uk/maps/@{},{},16z \n Температура воздуха: {}°C \n {} \n Скорость ветра: {}м/c \n Влажность: {}% \n Давление: {}".format(msgGeoString, geoLat, geoLng, geoLat, geoLng, forecastp2, forecastp2Summary, forecastp2Windspeed, forecastp2Hum*100, forecastp2Pressure)
                    msgsend(userid, vk_message, chat_id)

                else:
                    vk_message = "Не знаю такого места!"
                    msgsend(userid, vk_message, chat_id)



            #vk_message = "successful!"
            #msgsend(userid, vk_message, chat_id)
    elif msg in msg_calc:
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
                vk_message = "Неправильный ввод! Вы ввели: " + str(msg)
                msgsend(userid, vk_message, chat_id)
        except Exception:
            vk_message = "Неправильный ввод! Пример: 7 + 3, 51 / 3"
            msgsend(userid, vk_message, chat_id)
    elif msg in msg_truth:
        pravdamsg = []
        goodmsg = ["🎱Абсолютно!", "🎱Абсолютно точно!", "🎱Верно!", "🎱Правда!", "🎱Конечно же да!", "🎱Бесспорно.", "🎱Думаю да."]
        neutralmsg = ["🎱Возможно.", "🎱Не уверен.", "🎱Лучше не рассказывать.", "🎱Весьма сомнительно."]
        badmsg = ["🎱Скорее всего нет.", "🎱Врядли.", "🎱Что-то мне подсказывает, что нет.", "🎱Конечно нет.", "🎱Перспективы не очень хорошие.", "🎱Неправда. "]
        
        pravdamsg = goodmsg + neutralmsg + badmsg

        pravdafinal = random.choice(pravdamsg)
        vk_message = str(pravdafinal)
        msgsend(userid, vk_message, chat_id)
    elif msg in msg_stats:
        try:
            print("Stats get")
            userStats = table.find_one(vid=userid)
            vk_message = "Здравствуйте, {}, вы написали {} сообщений с момента включения бота.".format(theName,userStats["vcount"])
            msgsend(userid, vk_message, chat_id)
        except Exception:
            traceback.print_exc()


    elif msg in msg_imagetest:
        try:
            imagetestContent = uploadImage()
            vk_message = ""
            msgsend(userid, vk_message, chat_id, imagetestContent[0]["id"])
        except:
            traceback.print_exc()

    #else:
    #    if chatMode == 2:


def uploadImage():
    uploadURL = vkapi.photos.getUploadServer(album_id = albumID)
    uploadRequest = requests.post(uploadURL["upload_url"], files={"file1": open('photo.jpg', 'rb')})
    print uploadRequest
    uploadContent = uploadRequest.json()    
    uploadSave = vkapi.photos.save(album_id = albumID, server=uploadContent["server"], photos_list=uploadContent["photos_list"], hash=uploadContent["hash"])
    return uploadSave



def msgsend(userid, message, chatid, photoID=None):
    try:
        atest = result2[7]["from"]
        try:
            if int(userid) in blacklist:
                pass
                #message = message + customMsg + str(attempt_id)
                #vkapi.messages.send(chat_id = chat_id, message = message)
            else:
                if photoID != None:
                    message = message + customMsg + str(attempt_id)
                    readyphotoID = "photo" + str(ownerID) + "_" + str(photoID)
                    print(readyphotoID)
                    vkapi.messages.send(chat_id = chat_id, message = message, attachment=readyphotoID)
                    #print(str(datetime.now()))
                else:
                    message = message + customMsg + str(attempt_id)
                    print("NO IMAGE")
                    vkapi.messages.send(chat_id = chat_id, message = message)
                    #print(str(datetime.now()))
        except Exception:
            #traceback.print_exc()
            pass
    except KeyError:
        try:            
            message = message + customMsg + str(attempt_id)
            vkapi.messages.send(message = message, user_id = userid)
            #print(str(datetime.now()))
        except Exception:
            #traceback.print_exc()
            pass
        pass


#urlstring = "http://" + str(asd["server"]) + "?act=a_check&key=" + str(asd["key"]) + "&ts=" + str(asd["ts"]) + "&wait=25&mode=2"
#asd = vkapi.messages.getLongPollServer(use_ssl = 0)
#аurlstring = "http://" + str(asd["server"]) + "?act=a_check&key=" + str(asd["key"]) + "&ts=" + str(asd["ts"]) + "&wait=25&mode=2"
print("Connecting...")

while True:
    try:

        asd = vkapi.messages.getLongPollServer(use_ssl = 0)

        urlstring = "http://" + str(asd["server"]) + "?act=a_check&key=" + str(asd["key"]) + "&ts=" + str(asd["ts"]) + "&wait=25&mode=2"

        response = requests.get(urlstring).json()



        response = response["updates"][0]

        result2 = response

        if connect_success == 0:
            print("Ax3 Bot successfully connected!")
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
            #print profiles[0]['first_name'] + " " + profiles[0]['last_name']
            if str(result2[3])[:3] == "200":
                chat_id = chatidcheck(result2[3])
            print(str(result2[6]))




            msgcheck(str(result2[6]))
    except Exception:
        #traceback.print_exc()
        pass