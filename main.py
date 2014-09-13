# -*- coding: utf-8 -*-
import vk
import time, threading
import requests
import json
import ast
import traceback
import random
from datetime import datetime
from random import randint
from configobj import ConfigObj

weather_disable = 0 

print "Initializing..."
config = ConfigObj("settings.ini")
vk_access_token = config['vk_token']
geocodingAPI = config['google_geocoding']
forecastioAPI = config['forecastio']

helpMessage = (" - Помощь - \n"
    "test \n"
    "привет \n"
    "курс \n"
    "погода (ГОРОД) \n"
    "сосчитать (13 * 37) \n"
    "правда (что-то) \n"
    )

attempt_id = 0
chat_id = 0
#### Settings
customMsg = "\n //ax3bot "
show_names = 0 # 1 or 0, disable it for better performance
#### Settings
connect_success = 0


vkapi = vk.API(access_token=vk_access_token)
asd = vkapi.messages.getLongPollServer(use_ssl = 0)

def chatidcheck(chatcheck):
	chatcheckid = str(chatcheck)[-2:]
	return chatcheckid

def msgcheck(msg):
    global chat_id
    global attempt_id
    attempt_id = attempt_id + 1 # VK anti-block system
    if msg.find("test") == 0:
        vk_message = "Рандом: {}".format(str(randint(2,100))) + "%."
        msgsend(userid, vk_message, chat_id)
    elif msg.find("помощь") == 0:
        msgsend(userid, helpMessage, chat_id)
    elif msg.find("привет") == 0:
        vk_message = "Привет!" 
        msgsend(userid, vk_message, chat_id)
    elif msg.find("курс") == 0:
        kurs = requests.get("http://api.fixer.io/latest?base=USD")
        print kurs.json()
        kursbid1 = kurs.json()["rates"]
        kursbid = kursbid1["RUB"]
        vk_message = "Курс рубля к доллару: {} рублей = 1$.".format(kursbid)
        msgsend(userid, vk_message, chat_id)
    elif msg.find("погода") == 0:
        if weather_disable == 0:
            print "got it!"
            msgGeoSplit = msg.split()
            msgGeoSplit = msgGeoSplit[1:]
            msgGeoString = ' '.join(msgGeoSplit)
            print msgGeoString
            geocodeURL = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(msgGeoString, geocodingAPI)
            print geocodeURL
            geocodeRequest = requests.get(geocodeURL)
            geoResult2 = geocodeRequest.json()

            if geoResult2["status"] == "OK":
                geoResult = geoResult2["results"]
                geoLocation1 = geoResult[0]["geometry"]
                geoLocation2 = geoLocation1["location"]
                geoLat = geoLocation2["lat"]
                geoLng = geoLocation2["lng"]
                print "Lat: {}, Lng: {}".format(geoLat, geoLng)

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
    elif msg.find("сосчитать") == 0:
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
    elif msg.find("правда") == 0:
        pravdamsg = []
        goodmsg = ["🎱Абсолютно!", "🎱Абсолютно точно!", "🎱Верно!", "🎱Правда!", "🎱Конечно же да!", "🎱Бесспорно.", "🎱Думаю да."]
        neutralmsg = ["🎱Возможно.", "🎱Не уверен.", "🎱Лучше не рассказывать.", "🎱Весьма сомнительно."]
        badmsg = ["🎱Скорее всего нет.", "🎱Врядли.", "🎱Что-то мне подсказывает, что нет.", "🎱Конечно нет.", "🎱Перспективы не очень хорошие.", "🎱Неправда. "]
        
        pravdamsg = goodmsg + neutralmsg + badmsg

        pravdafinal = random.choice(pravdamsg)
        vk_message = str(pravdafinal)
        msgsend(userid, vk_message, chat_id)



def msgsend(userid, message, chatid):
    try:
        atest = result2[7]["from"]
        try:
            message = message + customMsg + str(attempt_id)
            vkapi.messages.send(chat_id = chat_id, message = message)
        except Exception:
            print "Message send error!"
            pass
    except KeyError:
        try:            
            message = message + customMsg + str(attempt_id)
            vkapi.messages.send(message = message, user_id = userid)
        except Exception:
            traceback.print_exc()
            print "Message send error!"
            pass
        pass


urlstring = "http://" + str(asd["server"]) + "?act=a_check&key=" + str(asd["key"]) + "&ts=" + str(asd["ts"]) + "&wait=25&mode=2"
print "Connecting..."

while True:
    try:
        asd = vkapi.messages.getLongPollServer(use_ssl = 0)
        urlstring = "http://" + str(asd["server"]) + "?act=a_check&key=" + str(asd["key"]) + "&ts=" + str(asd["ts"]) + "&wait=25&mode=2"
        response = requests.get(urlstring)
        result = ast.literal_eval(response.content)
        string2 = response.content[6]
        if connect_success == 0:
            print "Ax3 Bot successfully connected!"
            connect_success = 1
    except Exception:
        traceback.print_exc()
        pass
    try:
        result2 = result["updates"][0]
        if result2[0] == 4:
            try:
                userid = result2[7]["from"]
            except Exception:
                userid = result2[3]
                pass
            if show_names == 1:
                try:
                    profiles = vkapi.users.get(user_id=userid)
                except Exception:
                    print "--- User get failed!"
                    pass
                print profiles[0]['first_name'] + " " + profiles[0]['last_name']
            if str(result2[3])[:3] == "200":
                chat_id = chatidcheck(result2[3])
            print str(result2[6]).decode("utf-8")
            msgcheck(str(result2[6]))
    except Exception:
        pass