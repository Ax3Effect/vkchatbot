# -*- coding: utf-8 -*-

from random import randint
from time import strftime
import random
import time
import threading
import requests





def init():
    try:
        global textFiles
        global textFileUnavailable
        with open('textFile.txt', encoding="utf-8") as f:
            textFiles = f.readlines()
        textFileUnavailable = False
    except Exception:
        textFileUnavailable = True

def RateLimited(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rateLimitedFunction(*args,**kargs):
            elapsed = time.clock() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait>0:
                time.sleep(leftToWait)
            ret = func(*args,**kargs)
            lastTimeCalled[0] = time.clock()
            return ret
        return rateLimitedFunction
    return decorate



def respond_to(message_to):
    def wrapper(func):
        def responding_to(*args, **kwargs):
            msg_wrap = args[0]["msg"]
            if msg_wrap.split(' ')[0].lower() in message_to: 
                return func(*args, **kwargs)
        return responding_to
    return wrapper


ALL_FUNCTIONS = ["msg_test", "msg_hi", "msg_truth", "msg_chatmode", "msg_infa"] # СЮДА ОБЯЗАТЕЛЬНО ДОБАВИТЬ НАЗВАНИЕ НОВОЙ ФУНКЦИИ
ALL_CHATMODS = {"1":"chat_huf", "2":"chat_custom_texts"} # А СЮДА НАЗВАНИЕ ФУНКЦИИ ЧАТМОДА

def return_functions():
    return ALL_FUNCTIONS

def return_chatmods():
    return ALL_CHATMODS

@respond_to(["тест","test"])
def msg_test(msg):
    return {"msg":"test", "photo_id":"photo286006014_370245189"}
    #return "Test success {} %.".format(str(randint(2,100)))

@respond_to(["привет", "ку", "hi"])
def msg_hi(msg):
    return "Привет!\n Напиши мне слово 'помощь', чтобы узнать список команд."

@respond_to(["помощь"])
def msg_help(msg):
    return "👹"

@respond_to(["правда"])
def msg_truth(msg):
    pravdamsg = []
    goodmsg = ["🎱Абсолютно!", "🎱Абсолютно точно!", "🎱Верно!", "🎱Правда!", "🎱Конечно же да!", "🎱Бесспорно.", "🎱Думаю да."]
    neutralmsg = ["🎱Возможно.", "🎱Не уверен.", "🎱Лучше не рассказывать.", "🎱Весьма сомнительно."]
    badmsg = ["🎱Скорее всего нет.", "🎱Врядли.", "🎱Что-то мне подсказывает, что нет.", "🎱Конечно нет.", "🎱Перспективы не очень хорошие.", "🎱Неправда. "]
    pravdamsg = goodmsg + neutralmsg + badmsg
    pravdafinal = random.choice(pravdamsg)
    return {"msg":pravdafinal, "msg_id":msg["msg_id"]}

@respond_to(["чатмод", "chatmode"])
def msg_chatmode(msg):
    msg_edit = msg["msg"].split()
    msg_edit1 = int(msg[1])
    try:
        probability = int(msg[2])
    except Exception:
        probability = 1
    try:
        photo_probability = int(msg[3])
    except Exception:
        photo_probability = 1
    #if int(userid) == int(controlID):
    autoChatMode = msg_edit1
    vk_message = "// Режим чата сменен на: " + str(msg_edit1) + ", вероятность:" + str(probability) + ", вероятность фото: " + str(photo_probability)
    return {"msg":vk_message, "CHANGE_chatmode":autoChatMode, "CHANGE_probability":probability, "CHANGE_photo_probability":photo_probability}

@respond_to(["инфа","инфа,"])
def msg_infa(msg):
    msg = msg["msg"]
    msgInfa = msg.split()

    msgInfa = msgInfa[1:]
    if msgInfa[0] == "что":
        msgInfa.pop(0)
    
    msgInfa = ' '.join(msgInfa)
    vk_message = "Инфа, что {} - {}%. ".format(msgInfa, str(randint(2,100)))
    return vk_message

def chat_huf(msg):
    huifURL = "http://huifikator.ru/api.php?text=" + str(msg["msg"])
    huifGet = requests.get(huifURL)
    huifGet = huifGet.text
    return str(huifGet)

@RateLimited(1)
def chat_custom_texts(msg):
    if textFileUnavailable == False:
        probability = msg["probability"]
        photo_probability = msg["photo_probability"]

        random_msg = random.random()
        random_photo = random.random()
        if random_msg < float(probability):
            chosenMsg = random.choice(textFiles) 

            if random_photo < float(photo_probability):
                photo_list = ["photo286006014_371428465"]
                chosenPhoto = random.choice(photo_list)
                return {"msg":chosenMsg, "photo_id":chosenPhoto}
            else:
                return {"msg":chosenMsg}
            pass









