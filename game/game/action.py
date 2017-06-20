#!/usr/bin/python
# -*- coding: utf-8 -*-


import base64, json
import SocketServer
from security import SecurityTools as SecTools
from log import LoggerTools as Log
from data import DataDriver
from user import User

import  Queue
import time
import configure

class Action(object):
    """负责接受用户的行为信息，用udp"""

    def __init__(self):
        pass

    def ActionMsgDispatcher(self, msg, socket, client_address):
        #assert msg[u'name'] != u''  "blank Action"
        try:
            #print msg
            token = msg[u'name']
            #token = SecTools.AESDecrypt(token)
        except:
            Log.info("wrong msg parsing ")
        try:
            while not self.__logout_user.empty():
                username = self.__logout_user.get()
                if username:
                    print "user %s over" % username
                    del self.__users[username]
        except:
            Log.error("Error: userinfo delete failure")

        action = msg.get(u'action')

        if not action and client_address == (configure.MOSTER_HOST, configure.MONSTER_PORT):
            monsteraction = msg[u'monsteraction']
            print "hello"
            msg = {'monsteraction': monsteraction, 'socket': socket}
            if token == "":
                for user in self.__users.values():
                    user.AddMonsterMsg(msg)
            else:
                user = self.__users.get(token)
                user.AddMonsterMsg(msg)
            return
        if not self.__users.get(token, None):
            try:
                user = User()
                user.Init(token, client_address, self.AddLogoutUser)
                self.__users[token] = user
            except:
                Log.error("Error: user  %s init failure" % token)
        try:
            loginTime = self.__users.get(token).login_time
            if loginTime:
                action = msg.get(u'action')
                tomd5 = action[u"operate"] + action[u'para1'] + action[u'para2'] + loginTime
                if base64.b64encode(SecTools.EnHash(tomd5.encode("utf-8"))) ==  msg[u'md5']:
                    user = self.__users.get(token)
                    msg = {'action':action,'socket':socket,'client_address':client_address}
                    if user:
                        user.AddMsg(msg)
        except:
            Log.error("Error: %s msg put into user msgqueue failure" % token)


    def ActionHandler(self, HandlerUDPMessage):
        class MyActionHandler(SocketServer.BaseRequestHandler):
            def handle(self):
                data = self.request[0]
                socket = self.request[1]
                try:
                    message = json.loads(data)
                except Exception, e:
                    Log.error("faild to parse action info")
                    Log.error(e.message)
                HandlerUDPMessage(message, socket, self.client_address)
        return MyActionHandler

    #user线程用一个logout队列与主线程通信，
    #用户退出时把自己的id放入队列中，主线程从user队列中清除已退出的user对象
    def AddLogoutUser(self, username):
        self.__logout_user.put(username)

    #初始化action进程
    def ActionServer(self):
        Log.Init()
        DataDriver.InitDB()
        self.__users = {} #token为key，user为value，user里面存队列
        self.__logout_user = Queue.Queue()
        actionServer = SocketServer.UDPServer((configure.ACTION_HOST, configure.ACTION_PORT), self.ActionHandler(self.ActionMsgDispatcher))
        actionServer.serve_forever()
