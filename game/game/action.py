#!/usr/bin/python
# -*- coding: utf-8 -*-


import base64, json
import SocketServer
from security import SecurityTools as SecTools
from log import LoggerTools as Log
from data import DataDriver
from user import User
from configure import *

class Action(object):
    """负责接受用户的行为信息，用udp"""

    def __init__(self):
        pass

    def ActionMsgDispatcher(self, msg, socket, client_address):
        assert msg[u'name'] != u'' and msg[u'action'] != u''  "blank Action"
        token = msg[u'name']
        action = msg[u'action']

        #if token not in self.__users.keys():
        if not self.__users.get(token, None):
            try:
                user = User()
                user.Init(token, client_address)
                self.__users[token] = user
                self.__thread.append(user.userthread)
            except Exception, e:
                Log.error("Error: user  %s init failure" % token)
                Log.error(e.message)
        try:
            user = self.__users[token]
            loginTime = user.login_time
            tomd5 = action[u"operate"] + action[u'para1'] + action[u'para2'] + loginTime
            if loginTime:
                #load = false
                if base64.b64encode(SecTools.EnHash(tomd5.encode("utf-8"))) == msg[u'md5']:
                    msg = {'action':action,'socket':socket,'client_address':client_address}
                    user.AddMsg(msg)
                else:
                    logininfo = DataDriver.GetLoginInfo(token)
                    loginTime = logininfo['logintime']

        except Exception, e:
            Log.error("Error: %s msg put into user msgqueue failure" % token)
            Log.error(e.message)




    def ActionHandler(self, HandlerUDPMessage):
        class MyActionHandler(SocketServer.BaseRequestHandler):
            """
            This class works similar to the TCP handler class, except that
            self.request consists of a pair of data and client socket, and since
            there is no connection the client address must be given explicitly
            when sending data back via sendto().
            """
            def handle(self):
                data = self.request[0]
                socket = self.request[1]
                try:
                    message = json.loads(data)
                except Exception, e:
                    Log.error("faild to parse action info")
                    Log.error(e.message)
                HandlerUDPMessage(message, socket, self.client_address)
                #print self.server.socket

                #print socket
                #print self.client_address
                #print "{} wrote:".format(self.client_address[0])
                #socket.sendto(json.dumps(message), self.client_address)

        return MyActionHandler

    def ActionServer(self):
        Log.Init()
        DataDriver.InitDB()
        self.__users = {} #token为key，user为value，user里面存队列
        self.__thread = []
        actionServer = SocketServer.UDPServer((ACTION_HOST, ACTION_PORT), self.ActionHandler(self.ActionMsgDispatcher))
        actionServer.serve_forever()