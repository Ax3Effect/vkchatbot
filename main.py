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
config = ConfigObj("settings.ini")
vk_access_token = config['vk_token']
attempt_id = 0
chat_id = 0

#### Settings
customMsg = "\n //ax3bot"
show_names = 0 # 1 or 0, disable it for better performance
#### Settings


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
        vk_message = "Рандом: " + str(randint(2,100)) + "%." + "\n id: " + str(attempt_id)
        msgsend(userid, vk_message, chat_id)
    elif msg.find("привет") == 0:
        vk_message = "Привет!" + "\n id: " + str(attempt_id)
        msgsend(userid, vk_message, chat_id)
    elif msg.find("курс") == 0:
        kurs = requests.get("http://api.fixer.io/latest?base=USD")
        print kurs.json()
        kursbid1 = kurs.json()["rates"]
        kursbid = kursbid1["RUB"]
        vk_message = "Курс рубля к доллару: " + str(kursbid) + " рублей = 1$" + "\n id: " + str(attempt_id)
        msgsend(userid, vk_message, chat_id)
    #elif msg.find("погода") == 0:
        #obs = owm.weather_at('Moscow,ru')
        #w = obs.get_weather()
        #temp = w.get_temperature(unit='celsius')
        #vk_message = "Температура в Москве: " + str(temp["temp"]) + " градусов." + "\n id: " + str(attempt_id)
        #msgsend(userid, vk_message, chat_id)
        #pass
    elif msg.find("сосчитать") == 0:
        msgCalc = msg.split()
        msgCalc = msgCalc[1:]
        print "--------" + str(msgCalc)
        try:
            if msgCalc[1] == "+":
                msgCalcResult = int(msgCalc[0]) + int(msgCalc[2])
                vk_message = "Результат: " + str(msgCalcResult)
                msgsend(userid, vk_message, chat_id)
            elif msgCalc[1] == "-":
                msgCalcResult = int(msgCalc[0]) - int(msgCalc[2])
                vk_message = "Результат: " + str(msgCalcResult)
                msgsend(userid, vk_message, chat_id)
            elif msgCalc[1] == "*":
                msgCalcResult = int(msgCalc[0]) * int(msgCalc[2])
                vk_message = "Результат: " + str(msgCalcResult)
                msgsend(userid, vk_message, chat_id)
            elif msgCalc[1] == "/":
                msgCalcResult = int(msgCalc[0]) / int(msgCalc[2])
                vk_message = "Результат: " + str(msgCalcResult)
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
            message = message + customMsg
            vkapi.messages.send(chat_id = chat_id, message = message)
        except Exception:
            print "Message send error!"
            pass
    except KeyError:
        try:            
            message = message + customMsg
            vkapi.messages.send(message = message, user_id = userid)
        except Exception:
            traceback.print_exc()
            print "Message send error!"
            pass
        pass


urlstring = "http://" + str(asd["server"]) + "?act=a_check&key=" + str(asd["key"]) + "&ts=" + str(asd["ts"]) + "&wait=25&mode=2"
print "Ax3 VK Bot activated!"

while True:
    try:
        asd = vkapi.messages.getLongPollServer(use_ssl = 0)
        urlstring = "http://" + str(asd["server"]) + "?act=a_check&key=" + str(asd["key"]) + "&ts=" + str(asd["ts"]) + "&wait=25&mode=2"
        response = requests.get(urlstring)
        result = ast.literal_eval(response.content)
        string2 = response.content[6]
    except Exception:
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