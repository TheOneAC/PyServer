#!/usr/bin/python
# -*- coding: UTF-8 -*-
import Queue
from data import DataDriver
from log import LoggerTools as Log
import threading
import  json, time



class User:
    '''一个玩家，包括玩家的物品，任务进度，位置，血量，装备等所有信息'''
    def __init__(self):
        self.__queue = Queue.Queue()
        self.__name = u"zero"
        self.__password = None
        self.__position = ()
        self.__missions = {}
        self.__equip = []
        self.__items = {}
        self.token = u''
        self.sign = u''
        self.__login_time = u''
        self.__userthread = None
        self.__client_address = u''
        self.__socket = None

    def name():
        doc = u"用户名"
        def fget(self):
            return self.__name
        def fset(self, value):
            self.__name = value
        def fdel(self):
            del self.__name
        return locals()
    name = property(**name())

    def password():
        doc = u"密码"
        def fget(self):
            return self.__password
        def fset(self, value):
            self.__password = value
        def fdel(self):
            del self.__password
        return locals()
    password = property(**password())
    
    def position():
        doc = u"位置坐标"
        def fget(self):
            return self.__position
        def fset(self, value):
            self.__position = value
        def fdel(self):
            del self.__position
        return locals()
    position = property(**position())

    def missions():
        doc = u"任务."
        def fget(self):
            return self.__missions
        def fset(self, value):
            self.__missions = value
        def fdel(self):
            del self.__missions
        return locals()
    missions = property(**missions())

    def equip():
        doc = u"装备"
        def fget(self):
            return self.__equip
        def fset(self, value):
            self.__equip = value
        def fdel(self):
            del self.__equip
        return locals()
    equip = property(**equip())

    def items():
        doc = u"物品"
        def fget(self):
            return self.__items
        def fset(self, value):
            self.__items = value
        def fdel(self):
            del self.__items
        return locals()
    items = property(**items())

    def login_time():
        doc = u"登录时间"
        def fget(self):
            return self.__login_time
        def fset(self, value):
            self.__items = value
        def fdel(self):
            del self.__login_time
        return locals()
    login_time = property(**login_time())

    def userthread():
        doc = u"用户线程"
        def fget(self):
            return self.__userthread
        def fset(self, value):
            self.__userthread = value
        def fdel(self):
            del self.__userthread
        return locals()
    userthread = property(**userthread())

    def DumpUserInfo(self,username):
        userinfo = users.save({u'name':self.__name, u'password':self.__password,
                               u'equip':[3001], u'items':items, u'missions':{}, u'coordinate':(0,0)})
        DataDriver.DumpUserInfo(username, userinfo)


    #由action线程调用，添加msg
    def AddMsg(self, msg):
        self.__queue.put(msg)

    #读取自己的msg，并处理，同时负责定时存储
    def StartUser(self, token):
        #worktime = time.
        while True:
            #if time.time()
            if not self.__queue.empty():
                msg = self.__queue.get()
                socket = msg[u'socket']
                if socket != self.__socket:
                    self.__socket = socket
                client_address = msg[u'client_address']
                if client_address != self.__client_address:
                    self.__client_address = client_address
                if msg[u'action'] and msg[u'action'][u'operate'] == "":
                    print u"心跳"
                    continue
                elif msg[u'action'] and msg[u'action'][u'operate'] != "end":
                    #print  msg['action']
                    #socket.sendto(json.dumps(msg['action']), self.__client_address)
                    #把action传进去具体处理
                    self.ProcessAction(msg[u'action'])
                else:
                    if not msg[u'action']:
                        Log.debug(u'action不见了')
                    break
        ####写回数据库
        self.DumpUserInfo(token)

    #处理action，action由用户线程从msg里面取出来
    def ProcessAction(self, action):
        if action[u'operate'] == "move":
            self.__position = (action[u'para1'], action[u'para2'])
            action[u'operate'] = "position"
            print u"发送"
            xxx = self.__socket.sendto(json.dumps(action), self.__client_address)
            print xxx
            print json.dumps(action)


    def Init(self, token, client_address):
        try:
            userinfo = DataDriver.GetUserInfo(token)
            logintime = DataDriver.GetLoginInfo(token)
        except:
            Log.error("Error: Get info for %s from DB failure" % token)
        try:
            self.__name = userinfo[u'name']
            self.__password = userinfo[u'password']
            self.__position = userinfo[u'coordinate']
            self.__missions = userinfo[u'missions']
            self.__equip = userinfo[u'equip']
            self.__items = userinfo[u'items']
            self.__login_time = logintime[u'logintime']
            self.__client_address = client_address
        except:
            Log.error("Error: userinfo cached in server for %s failure" % token)
        try:
            userthread = threading.Thread(target=self.StartUser,args= (token,))
            userthread.setDaemon(True)
            userthread.start()
            self.__userthread = userthread
        except:
            Log.error("Error: unable to start thread for %s" % token)

if __name__ == "__main__":
    user = User()
    user.Init("zero")
    print user.name


    



