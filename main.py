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

Заходите в папку /plugins/base_functions.py и пишите @respond_to("прикол") перед функцией, которая будет вызываться!

@respond_to("прикол")
def prikol(msg):
    return "123123"

Потом обязательно ищем "ALL_FUNCTIONS" и вписываем ИМЯ ФУНКЦИИ туда! Иначе не будет работать.


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
import logging
import http.client
'''
http.client.HTTPConnection.debuglevel = 1

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
'''
print("VK Chat Bot от Ax3 (vk.com/ax3effect)")

#### Settings
blacklist = [] # blacklist, VK ID's
chat_blacklist = [] # chat blacklist, VK Chat ID's
probability = 1
photo_probability = 0.05

#### Settings

#### Config files
try:
    config = ConfigObj("settings.ini")
except Exception:
    print("Вы не вписали настройки для чат-бота. Найдите файл 'settings_example.ini', впишите токены и айди и переименуйте на 'settings.ini'.")
    sys.exit(1)
ADMIN_ID = int(config['admin_id'])

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
    try:
        albumID = config['album_id']
    except Exception:
        print("Не выставлено значение albumID. Загрузка фото не будет работать.")
        albumID = 0






print("Бот запускается...")



#### Variables
attempt_id = 0
chat_id = 0
weather_disable = 0 
global autoChatMode
autoChatMode = 0
redditCounter = 1
connect_success = 0
global prepareTextFile
global linesList
global changetxtids
prepareTextFile = 0
changetxtids = []



# VK API
vkapi = vk.API(access_token=vk_access_token)

#getting bot id
print("Берём айди бота... ", end="")
bot_info = vkapi.users.get()
OWNER_ID = bot_info[0]["id"]
print(": " + str(OWNER_ID))


def chatidcheck(chatcheck):
    chatcheck = str(chatcheck)[1:]
    counter = 0
 
    for i in list(chatcheck):
        counter = counter + 1
        if i != "0":
            return chatcheck[int(counter-1):]

def downloadImage(url):
    image_name = 'photo.jpg'
    urllib.request.urlretrieve(url, image_name)

'''
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
'''

# Friends add function
def friendsAdd():
    try:
        getRequests = vkapi.friends.getRequests()
        for eachFriend in getRequests["items"]:
            print("Added " + str(eachFriend) + " as a friend")

            vkapi.friends.add(user_id = eachFriend)
            time.sleep(10)
        time.sleep(70)
        friendsAdd()
    except Exception:
        time.sleep(20)
        friendsAdd()



t = threading.Thread(target = friendsAdd)
t.start()




# ---------- Message Check Function --------

def msgcheck(msg, id=None):
    noMessageDetected = True
    autoChatMode = msg.get('chat_mode', 0)
    probability = msg.get('probability')
    photo_probability = msg.get('photo_probability')

    for x in all_functions: 
        methodToCall = getattr(base_functions, x)
        result = methodToCall(msg)
        #print(str(type(result))+ " - " + str(result))
        if result is not None:
            noMessageDetected = False
            if type(result) is str: 
                msgsend(user_id, result, chat_id)
            elif type(result) is dict:
                try:
                    message = result.get('msg')
                    photo_id = result.get('photo_id', None)
                    audio_id = result.get('audio_id', None)
                    if result.get('CHANGE_chatmode', None) is not None:
                        autoChatMode = result.get('CHANGE_chatmode', None)
                    msg_id = result.get('msg_id')
                    if result.get('CHANGE_probability', None) is not None:
                        probability = result.get('CHANGE_probability')
                        photo_probability = result.get('CHANGE_photo_probability')

                    msgsend(user_id, message, chat_id, photo_id, audio_id, None)

                except Exception:
                    traceback.print_exc()
                    pass
    if noMessageDetected:
        chosen_chatmode = all_chatmods.get(str(autoChatMode), None)
        if chosen_chatmode is not None:
            methodToCall = getattr(base_functions, chosen_chatmode)
            result = methodToCall(msg)
            if result is not None:
                if type(result) is str: 
                    msgsend(user_id, result, chat_id)
                elif type(result) is dict:
                    try:
                        message = result.get('msg')
                        photo_id = result.get('photo_id', None)
                        audio_id = result.get('audio_id', None)
                        msgsend(user_id, message, chat_id, photo_id, audio_id, None)
                    except Exception:
                        pass


    msgReturn = {}
    msgReturn["autoChatMode"] = autoChatMode
    msgReturn["probability"] = probability
    msgReturn["photo_probability"] = photo_probability
    return msgReturn






'''
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
'''
def safe_list_get(l, idx, default):
  try:
    return l[idx]
  except IndexError:
    return default

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
                    #readyphotoID = "photo" + str(ownerID) + "_" + str(photoID)
                    #print(readyphotoID)
                    readyphotoID = photoID
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
            print(vkerror)
            if str(vkerror).find("14. Captcha") == 0:
                print("[ОШИБКА] Капча нужна!")
                time.sleep(5)
                pass
    except KeyError:
        try:            
            if int(userid) in blacklist:
                pass
            if photoID != None:
                message = message + "\n\n" + customMsg + str(attempt_id)
                #readyphotoID = "photo" + str(ownerID) + "_" + str(photoID)
                readyphotoID = photoID
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







if __name__ == "__main__":


    from plugins import base_functions
    all_functions = base_functions.return_functions()
    all_chatmods = base_functions.return_chatmods()

    base_functions.init()
    







    connected = False
    while not connected:
        try:

            asd = vkapi.messages.getLongPollServer(use_ssl = 0) # getting all info for connection
            ts = asd["ts"]
            connected = True
        except Exception:
            print("Подключение...")
            time.sleep(1)
            pass
     # ts parameter for first msg getting
    # Main function
    while True:
        try:
            urlstring = "http://" + str(asd["server"]) + "?act=a_check&key=" + str(asd["key"]) + "&ts=" + str(ts) + "&wait=100&mode=2"
            response = requests.get(urlstring).json()
            ts = response["ts"] # ts for next request
            response = response["updates"][0] 
            result2 = response
            if connect_success == 0:
                print("Успешно подключено к ВК")
                connect_success = 1
        except Exception:
            pass
        try:
            
            if safe_list_get(result2, 0, None) == 4: # message received code 4 (message received)
                try:
                    user_id = result2[7]["from"] # chat message or user message
                except Exception:
                    user_id = result2[3]
                    pass


                if int(user_id) == int(OWNER_ID): #duplicate
                    pass
                else:
                    #if show_names == 1:

                    
                    if str(result2[3])[:3] == "200":
                        chat_id = chatidcheck(result2[3])
                    
                    #print(str(_bold(theName)) + ": " + str(result2[6]))
                    
                        #testt(str(result2[6]))
                        #print("before: " + str(autoChatMode))
                        msgDict = {}
                        msgDict["msg"] = str(result2[6])
                        msgDict["chat_id"] = chat_id
                        msgDict["msg_id"] = str(result2[1])
                        msgDict["user_id"] = user_id
                        msgDict["chat_mode"] = autoChatMode
                        msgDict["probability"] = probability
                        msgDict["photo_probability"] = photo_probability

                        # getting info back

                        msgReturn = msgcheck(msgDict)
                        autoChatMode = msgReturn["autoChatMode"]
                        probability = msgReturn["probability"]
                        photo_probability = msgReturn["photo_probability"]
                        #print("out of context : " + str(autoChatMode))


        except vk.api.VkAPIMethodError:
            traceback.print_exc()
            vk_message = "⚠ Загрузка не удалась."
            msgsend(userid, vk_message, chat_id)
        except Exception:
            traceback.print_exc()
            pass
