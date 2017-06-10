#!/usr/bin/python
# -*- coding: UTF-8 -*-
import Queue
from data import DataDriver
from log import LoggerTools as Log
import threading
import  json



class User:
    '''一个玩家，包括玩家的物品，任务进度，位置，血量，装备等所有信息'''
    def __init__(self):
        self.__queue = Queue.Queue()

        self.__name = "zero"
        self.__password = None
        self.__position = ()
        self.__missions = {}
        self.__equip = []
        self.__items = {}
        self.token = ''
        self.sign = ''
        self.__login_time = ''
        self.__socket = ''
        self.__client_address = ''

    def name():
        doc = "用户名"
        def fget(self):
            return self.__name
        def fset(self, value):
            self.__name = value
        def fdel(self):
            del self.__name
        return locals()
    name = property(**name())

    def password():
        doc = "密码"
        def fget(self):
            return self.__password
        def fset(self, value):
            self.__password = value
        def fdel(self):
            del self.__password
        return locals()
    password = property(**password())
    
    def position():
        doc = "位置坐标"
        def fget(self):
            return self.__position
        def fset(self, value):
            self.__position = value
        def fdel(self):
            del self.__position
        return locals()
    position = property(**position())

    def missions():
        doc = "任务."
        def fget(self):
            return self.__missions
        def fset(self, value):
            self.__missions = value
        def fdel(self):
            del self.__missions
        return locals()
    missions = property(**missions())

    def equip():
        doc = "装备"
        def fget(self):
            return self.__equip
        def fset(self, value):
            self.__equip = value
        def fdel(self):
            del self.__equip
        return locals()
    equip = property(**equip())

    def items():
        doc = "物品"
        def fget(self):
            return self.__items
        def fset(self, value):
            self.__items = value
        def fdel(self):
            del self.__items
        return locals()
    items = property(**items())

    def login_time():
        doc = "登录时间"
        def fget(self):
            return self.__login_time
        def fset(self, value):
            self.__items = value
        def fdel(self):
            del self.__login_time
        return locals()
    login_time = property(**login_time())

    #由action线程调用，添加msg
    def AddMsg(self, msg):
        self.__queue.put(msg)

    #读取自己的msg，并处理，同时负责定时存储
    def StartUser(self, token):
        while True:
            if not self.__queue.empty():
                msg = self.__queue.get()
                socket = msg['socket']
                client_address = msg['client_address']
                if client_address != self.__client_address:
                    self.__client_address = client_address
                if msg['action'] != "end":
                    socket.sendto(json.dumps(msg['action']), self.__client_address)
                else:
                    pass
                print msg

    def init(self,token, client_address):
        try:
            userinfo = DataDriver.GetUserInfo(token)
            logintime = DataDriver.GetLoginInfo(token)
        except:
            Log.error("Error: Get info for %s from DB failure" % token)
        try:
            self.__name = userinfo['name']
            self.__password = userinfo['password']
            self.__position = userinfo['coordinate']
            self.__missions = userinfo['missions']
            self.__equip = userinfo['equip']
            self.__items = userinfo['items']
            self.__login_time = logintime['logintime']
            self.__client_address = client_address
        except:
            Log.error("Error: userinfo cached in server for %s failure" % token)
        try:
            userthread = threading.Thread(target=self.StartUser,args= (token,))
            userthread.start()
            self.__threadId = userthread.ident
        except:
            Log.error("Error: unable to start thread for %s" % token)

if __name__ == "__main__":
    user = User()
    user.init("zero")
    print user.name


    



