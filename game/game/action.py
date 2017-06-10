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
        assert msg[u'token'] != u'' and msg[u'action'] != u''  "blank Action"
        try:
            token = base64.b64decode(msg[u'token'])
            #token = SecTools.AESDecrypt(token)
            action = msg[u'action']
        except:
            Log.info("wrong msg parsing ")

        if token not in self.__users.keys():
            try:
                user = User()
                user.init(token, client_address)
                self.__users[token] = user
            except:
                Log.error("Error: user  %s init failure" % token)
        try:
            loginTime = self.__users.get(token).login_time
            if loginTime and base64.b64encode(SecTools.EnHash(str(json.dumps(action) + loginTime))) ==  msg[u'md5']:
                user = self.__users.get(token)
                msg = {'action':action,'socket':socket,'client_address':client_address}
                if user:
                    user.AddMsg(msg)
                else:
                    pass
        except:
            Log.error("Error: %s msg put into user msgqueue failure" % token)




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
                message = json.loads(data)
                socket = self.request[1]
                print "hhhhhh"
                HandlerUDPMessage(message,socket,self.client_address)
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
        actionServer = SocketServer.UDPServer((ACTION_HOST, ACTION_PORT), self.ActionHandler(self.ActionMsgDispatcher))
        actionServer.serve_forever()