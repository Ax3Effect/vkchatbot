# -*- coding: utf-8 -*-
# VK Chat bot by Nazar K. https://vk.com/ax3effect

import vk

import requests
from configobj import ConfigObj
from sqlalchemy.orm import sessionmaker
import db
from db import User, Namecases, Messages
from caching_query import FromCache
import threading
from pprint import pprint
import time
from queue import Queue
import random
from sqlalchemy import desc
import re
import sys, os
Session = sessionmaker(bind=db.engine)
session = Session()

from requests_futures.sessions import FuturesSession
fsession = FuturesSession()

import logging
logging.basicConfig(filename='log_vk.log',level=logging.INFO)


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

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


def slicedict(d, s):
    return {k:v for k,v in d.items() if k.startswith(s)}

class VK(object):
    """
    A base class for VK
    Contain functions which directly work with VK
    """
    def __init__(self, config=None):
        self.config = config
        self.pollConfig = {"mode": 66, "wait": 30, "act": "a_check"}
        self.pollServer = ""
        self.pollInitialzed = False
        self.online = False
        self.userID = 0
        self.methods = 0
        self.cache = {}
        self.queue = Queue(maxsize=60)
        self.cmd = Cmd()
        self.admin_id = config["admin_id"]
        self.blacklist = []
        self.captcha_needed = False
        self.captcha_img = None
        self.captcha_sid = None
        self.timeout = config["timeout"]
        if os.path.exists("debug.txt"):
            self.debug = True
        else:
            self.debug = False
        '''
        blacklist_query = session.query(User).filter_by(is_blacklisted=1)
        if blacklist_query:
            for row in blacklist_query:
                self.blacklist.append(row.id)
        '''
        self.threads = []


    def auth(self):
        self.session = vk.Session(access_token=self.config["vk_token"])
        self.vkapi = vk.API(self.session)
        try:
            self.bot_id = self.vkapi.users.get()[0]["uid"]
            print("Auth success. ID: " + str(self.bot_id))
        except vk.exceptions.VkAPIError as e:
            #print("Auth fail. plz check token in settings.ini")
            raise e
        except IndexError:
            print("Auth failed. Please check token in settings.ini")
            sys.exit(1)

    def initPoll(self):
        self.pollInitialized = False
        response = self.vkapi.messages.getLongPollServer()
        self.initPollServer = response
        self.pollServer = "http://{server}?act={act}&key={key}&ts={ts}&wait={wait}&mode={mode}".format(server=response["server"], 
            act=self.pollConfig["act"], key=response["key"], ts=response["ts"], wait=self.pollConfig["wait"],
            mode = self.pollConfig["mode"])

        self.pollTS = response["ts"]
        self.pollKey = response["key"]
        self.pollInitialized = True

    def updatePoll(self):
        self.pollServer = "http://{server}?act={act}&key={key}&ts={ts}&wait={wait}&mode={mode}".format(server=self.initPollServer["server"], 
            act=self.pollConfig["act"], key=self.initPollServer["key"], ts=self.pollTS, wait=self.pollConfig["wait"],
            mode = self.pollConfig["mode"])

    def getLostMessages(self, new_ts):
        request = vkapi.vkapi.messages.getLongPollHistory(ts=new_ts)
        return request

    def getLongPoll(self):

        response_exists = False
        while response_exists == False:
            try:

                response = fsession.get(self.pollServer).result().json()
            except Exception:
                response = None
                pass
            #print(response)
            if response:
                if response.get("updates", None):
                    if len(response["updates"]) != 0:
                        response_exists = True
                        #print(response)
                        #print(str(response["ts"]) + " - " + str(self.pollTS) + " = " + str(response["ts"] - self.pollTS))

                        self.pollTS = response["ts"]
                        self.updatePoll()

                        msgthread = threading.Thread(target=self.cmd.msg, args=(response,))
                        msgthread.start()
                        #self.threads.append(msgthread)
                        #self.cmd.msg(response)


    def getLongPoll_Message(self):

        response = self.getLongPoll()
        while response["updates"][0][0] != 4:
            response = self.getLongPoll()
        return response

    def addUser(self, uid):
        if session.query(User).filter_by(id=uid).first():
            #print("Юзер {} уже есть в базе данных".format(uid))
            pass
        else:
            data = self.vkapi.users.get(user_ids=uid, fields="screen_name")

            code = '''
                var user_id = ''' + str(uid) + ''';
                var nom = API.users.get({"user_ids": user_id});
                var gen = API.users.get({"user_ids": user_id, "name_case": "gen"});
                var dat = API.users.get({"user_ids": user_id, "name_case": "dat"});
                var acc = API.users.get({"user_ids": user_id, "name_case": "acc"});
                var ins = API.users.get({"user_ids": user_id, "name_case": "ins"});
                var abl = API.users.get({"user_ids": user_id, "name_case": "abl"});
                return nom + gen + dat + acc + ins + abl;
                 '''
            namecases_data = self.vkapi.execute(code=code)
            namecases = Namecases(nom=namecases_data[0]["first_name"] + " " + namecases_data[0]["last_name"],
                gen = namecases_data[1]["first_name"] + " " + namecases_data[1]["last_name"],
                dat = namecases_data[2]["first_name"] + " " + namecases_data[2]["last_name"],
                acc = namecases_data[3]["first_name"] + " " + namecases_data[3]["last_name"],
                ins = namecases_data[4]["first_name"] + " " + namecases_data[4]["last_name"],
                abl = namecases_data[5]["first_name"] + " " + namecases_data[5]["last_name"]
                )
            populate_data = User(id=uid, first_name=data[0]["first_name"], last_name=data[0]["last_name"], screen_name=data[0]["screen_name"],
                namecase=namecases)
            session.add(populate_data)
            session.commit()
            #print("Юзер {} {} успешно добавлен в базу данных".format(populate_data.first_name, populate_data.last_name))
    def send(self, msg):

        #self.send_queue(message=msg["message"], user_id=0, chat_id=msg["group_id"])
        self.queue.put(msg)
        pass
    
    def send_queue(self):

        # TODO CAPTCHA

        while True:
            if not self.queue.empty():
                val = self.queue.get()
                try:
                    vkapi.vkapi.messages.send(**val)
                    #logging.info('Sent message to {} - {}: '.format(val["user_id"], val["message"])
                    time.sleep(float(vkapi.timeout))
                except Exception as e:
                    #print(e)
                    #logging.error('Error: {}'.format(e))
                    if e.is_captcha_needed:
                        if e.captcha_sid != None:
                            print("captcha img : {} | {}".format(e.captcha_sid, e.captcha_img))
                            self.captcha_needed = True
                            self.captcha_sid = e.captcha_sid
                            self.captcha_img = e.captcha_img




                    pass

            time.sleep(0.15)

    def insert_message_db(self, data):
        if data.get("chat_id", None) == None:
            data["chat_id"] = 0
        populate_data = Messages(user_id=data["user_id"], chat_id=data["chat_id"], timestamp = data["timestamp"],
            message = data["message"])
        session.add(populate_data)
        session.commit()



class MessageEngine(object):
    def __init__(self, *args):
        self.rules = {}
        self.rules_user_id = {}
        self.rules_chat_id = {}
        self.rules_init = {}



    def add_command(self, rule, func):
        #print("Added rule " + str(rule))
        self.rules[rule] = func

    def add(self, rule):
        def decorator(func):
            self.add_command(rule, func)
            return func
        return decorator

    def init_function(self, rule):
        def decorator(func):
            response = func()
            self.rules_init[rule] = response
            return func
        return decorator



    def add_user_id(self, rule):
        def decorator(func):
            self.add_command_user_id(rule, func)
            return func
        return decorator

    def add_chat_id(self, rule):
        def decorator(func):
            self.add_command_chat_id(rule, func)
            return func
        return decorator

    def add_command_user_id(self, rule, func):
        #print("Added rule for user " + str(rule))
        self.rules_user_id[int(rule)] = func

    def add_command_chat_id(self, rule, func):
        #print("Added rule for chat " + str(rule))
        self.rules_chat_id[int(rule)] = func


    def run(self, commands, data):
        # priority:
        # 1 - command
        # 2 - user id
        # 3 - group id
        func = None
        for command in commands:
            command = command.lower()
            #func = self.rules.get(command, None) #exact search
            #func = slicedict(self.rules, command)
            for key in self.rules:
                if key in command:
                    if command.startswith(key):
                        func = self.rules[key]
                        break
                else:
                    func = None

            if func is not None:
                parameter = 'command_{}'.format(command)
                
                #print('{}->{}'.format(command, func))
                #print("param " + str(comma))
                return func(parameter, data)
        func = self.rules_user_id.get(int(data["user_id"]), None)
        if func is not None:
            parameter = 'command_{}'.format(command)
            #print('{}->{}'.format(command, func))
            return func(parameter, data)
        if data["chat_id"] is not None:
            func = self.rules_chat_id.get(int(data["chat_id"]), None)
            if func is not None:
                parameter = 'command_{}'.format(command)
                #print('{}->{}'.format(command, func))
                return func(parameter, data)

class Cmd(object):

    def __init__(self):
        self.msgengine = MessageEngine()
        pass

    def msg(self, response):
        #print(response)
        if response.get('history', None):
            #response["updates"] = response["history"]
            #print(response)
            if response["messages"][0] == 0:
                pass
            else:
                pass
                #print(response["messages"][1]["body"] + " - " + str(response["new_pts"]))

        else:

            if response.get("updates", None):
                if len(response["updates"][0]) > 4:
                    #print("GETTING " + str(response))
                    if response["updates"][0][4]:
                        #print(response)
                        if response["updates"][0][7].get("from", None):
                            self.uid = response["updates"][0][7]["from"]
                            self.groupChat = True
                        else:
                            self.uid = response["updates"][0][3]
                            self.groupChat = False

                        if response["updates"][0][2] == "547":
                            pass
                        else:
                            self.timestamp = response["updates"][0][4]
                            if self.groupChat:
                                self.group_id = abs(2000000000 - response["updates"][0][3])
                            self.message = response["updates"][0][6]
                            #pprint(self.message + " - " + str(response["ts"]))
                            vkapi.addUser(self.uid)
                            self.db = session.query(User).options(FromCache('default')).filter_by(id=self.uid).first()

                            data = {"message":self.message,
                            "user_id":self.uid,
                            "timestamp":self.timestamp,
                            #"group_id":self.group_id,
                            "db":self.db,
                            "dbsession":session
                            }
                            #logging.info('Got message from {} - {}'.format(self.uid, self.message))
                            if self.groupChat:
                                data["chat_id"] = self.group_id
                            else:
                                data["chat_id"] = None

                            vkapi.insert_message_db(data)

                            if response["updates"][0][7].get("source_act", None):

                                if response["updates"][0][7]["source_act"] == "chat_invite_user":
                                    msg = {"message":"Привет, {}!".format(self.db.first_name),
                                    "chat_id":self.group_id,
                                    "from":self.uid
                                    }
                                    vkapi.send(msg)

                                if response["updates"][0][7]["source_act"] == "chat_title_update":
                                    msg = {"message":"Классное название, {}! ".format(self.db.first_name),
                                    "chat_id":self.group_id,
                                    "from":self.uid
                                    }
                                    vkapi.send(msg)


                            checkmessage = self.msgengine.run(commands=[self.message], data=data) #check for keywords
                            #print(checkmessage)


                            if checkmessage is not None:

                                if type(checkmessage) is dict: #if its dict (more info)
                                    msg = checkmessage
                                    if self.groupChat == True:
                                        msg["chat_id"] = self.group_id
                                    else:
                                        msg["user_id"] = self.uid
                                    msg["forward_messages"] = response["updates"][0][1]

                                    

                                else: #if it's jsut a string (message)
                                    if self.groupChat == True:
                                        msg = {"message":checkmessage,
                                        "chat_id":self.group_id,
                                        "from":self.uid,
                                        }
                                    if self.groupChat == False:
                                        msg = {"message":checkmessage,
                                        "user_id":self.uid,
                                        "from":self.uid
                                        }

                                    msg["forward_messages"] = response["updates"][0][1]
                                if vkapi.debug:

                                    last_timestamp = session.query(Messages).options(FromCache('default')).order_by(Messages.id.desc()).limit(2)
                                    msg["message"] = msg.get("message", "") + "\nДЕБАГ ВЕРСИЯ!!!! НИЧЕГО НЕ БУДЕТ СОХРАНЯТЬСЯ!!!!! \n Последнее сообщение было {} секунд назад ".format(
                                        self.timestamp-last_timestamp[1].timestamp)
                                vkapi.send(msg)


config = ConfigObj("settings.ini", encoding='utf8')
vkapi = VK(config)
vkapi.auth()
#print(vkapi.vkapi.users.get(user_ids=1))

vkapi.initPoll()

#print(vkapi.pollServer)


def loop():
    while True:
        response = vkapi.getLongPoll()

'''
def restartEveryTime():
    time.sleep(1800)
    print("Restarting...")
    os._exit(1)

'''

'''
def setStatus():
    while True:
        minutes = 5
        minutes_in_sec = minutes * 60


        last_timestamp = session.query(Messages).options(FromCache('default')).order_by(Messages.id.desc()).limit(1)
        #timestamp_ago = last_timestamp[0].timestamp-minutes_in_sec
        timestamp_ago = int(time.time())-minutes_in_sec
        time_info = session.query(Messages).options(FromCache('default')).filter(timestamp_ago<last_timestamp[0].timestamp).count()
        update_time = time.strftime("%H:%M:%S")
        #vkapi.vkapi.status.set(text="Обработано за последние {} минут: {} сообщений. Обновлено в {}".format(minutes, time_info, update_time))
        #vkapi.vkapi.status.set(text="таймштапф 5 минут назад: {} таймштамп последнего сбщ: {}".format(timestamp_ago, last_timestamp[0].timestamp))
        time.sleep(float(minutes_in_sec))
'''

def friendsAdd():
    while True:
        try:
            getRequests = vkapi.vkapi.friends.getRequests()
            if getRequests != []:
                for eachFriend in getRequests:
                    print("Added " + str(eachFriend) + " as a friend")

                    vkapi.vkapi.friends.add(user_id = eachFriend)
                    time.sleep(10)
                time.sleep(40)
        except Exception:
            time.sleep(30)
            pass



#print(c.testcommand("success!!"))
#print(c.checkmsg("ffff"
'''
all_methods = dir(c)
for method in all_methods[:]:
    if str(method).startswith("__"):
        all_methods.remove(method)

all_methods.remove("init")
#for method in all_methods:
#    print(getattr(c, method)("123", "123"))
print(Commands.testcommand._decorators)
'''

threads = []
t = threading.Thread(target=loop)
send_loop = threading.Thread(target=vkapi.send_queue)
#restartEveryTime = threading.Thread(target=restartEveryTime)
friendsAdd = threading.Thread(target=friendsAdd)
#setStatus = threading.Thread(target=setStatus)
t.start()
send_loop.start()   
#restartEveryTime.start()
friendsAdd.start()
#setStatus.start()


msg = vkapi.cmd.msgengine

#  ---------- ПИШИТЕ КОММАНДЫ ЗДЕСЬ ---------


@msg.add('test')
def ttest(param, data):
    return {"attachment":"photo10399749_384808788"}

@msg.add("помощь")
def help(param, data):
    message = "Все доступные команды: \n"
    for key in msg.rules:
        message = message + str(key) + "\n"
    return message

'''
@msg.add('random_photo_pic')
def gubi(param, data):
    random_choice = random.choice(msg.rules_init["init_photos"])
    return {"attachment":"photo{}_{}".format(vkapi.bot_id, random_choice)}
'''

'''
@msg.add_chat_id('84')
def tttttttest(param, data):
    return "testerino"
'''


@msg.add('айди конфы')
def conf_id(param, data):
    if data.get("chat_id", None):
        return data["chat_id"]
    else:
        return {"attachment":"video174811191_170020157"}

@msg.add('курс')
def exchange_rate(param, data):
    kurs_usd = requests.get("http://api.fixer.io/latest?base=USD")
    kursbid_usd = kurs_usd.json()["rates"]["RUB"]
    kurs_euro = requests.get("http://api.fixer.io/latest?base=EUR")
    kursbid_euro = kurs_euro.json()["rates"]["RUB"]
    kurs_gbp = requests.get("http://api.fixer.io/latest?base=GBP")
    kursbid_gbp = kurs_gbp.json()["rates"]["RUB"]
    vk_message = "1 Доллар = {} руб. \n 1 Евро = {} руб. \n 1 Фунт = {} руб".format(kursbid_usd, kursbid_euro, kursbid_gbp)
    return vk_message

@msg.add('таймаут')
def set_timeout(param, data):
    if int(data["user_id"]) == vkapi.admin_id:
        timeout_value = int(data["message"].split()[1])
        vkapi.timeout = timeout_value
        vkapi.config["timeout"] = timeout_value
        vkapi.config.write()
        return "тaймаут успешно поставлен на {} секунд".format(timeout_value)

@msg.add('правда')
def truth_or_false(param, data):
    pravdamsg = []
    goodmsg = ["🎱Абсолютно!", "🎱Абсолютно точно!", "🎱Верно!", "🎱Правда!", "🎱Конечно же да!", "🎱Бесспорно.", "🎱Думаю да."]
    neutralmsg = ["🎱Возможно.", "🎱Не уверен.", "🎱Лучше не рассказывать.", "🎱Весьма сомнительно."]
    badmsg = ["🎱Скорее всего нет.", "🎱Врядли.", "🎱Что-то мне подсказывает, что нет.", "🎱Конечно нет.", "🎱Перспективы не очень хорошие.", "🎱Неправда. "]
    pravdamsg = goodmsg + neutralmsg + badmsg
    pravdafinal = random.choice(pravdamsg)
    vk_message = str(pravdafinal)
    return vk_message

'''
@msg.init_function("init_photos")
def init_kirill():
    album_id = #### PUT YOUR ALBUM ID HERE !
    photos = vkapi.vkapi.photos.get(owner_id=vkapi.bot_id, album_id=album_id)
    #print(photos)
    photos_list = []
    for i in photos:
        #print(i)
        #print(i["pid"])
        photos_list.append(i["pid"])
    return photos_list

'''

#print(msg.rules_init)


# ---------- НЕ ПИШИТЕ КОММАНДЫ ПОСЛЕ ЭТОЙ СТРОЧКИ -----------
vkapi.cmd.msgengine = msg
