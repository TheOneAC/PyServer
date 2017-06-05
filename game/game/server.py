#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time

import socket
import SocketServer
from multiprocessing import Process
import logging, traceback  

import json, base64
import Queue, threading

from user import User
from configure import *
from log import LoggerTools as Log
from security import SecurityTools as SecTools
from data import DataDriver

class Users(object):
    """所有玩家的集合,负责玩家登陆,同时实例化每一个玩家,放在列表中
    并接受每个玩家的请求,用多程"""
    
    def __init__(self):
        self.__tokenDict = {}
        self.__userMsgQueue = {}

    def GetUser(self, user_name):
        tmp = DataDriver.GetUserInfo(user_name)
        return tmp

    def CheckPassword(self, message):
        tokenMessage = None
        try:
            decode_message = json.loads(message)
            #print decode_message
            assert decode_message[u'name'] != u'' and decode_message[u'password'] != u''  u"filed"
        except:
            Log.info('login decode failed')
            
        try:    
            user_name = decode_message[u'name']
            user_server = self.GetUser(user_name)
            if user_server and user_server[u'password'] == decode_message[u'password']:
                Log.info("new user: %s login success" % user_name)
                token = user_name + ' ' + str(time.time())
                token = token.encode('utf-8')
                en_token, signature = SecTools.Encrypt(token)
                token_message = {"token": en_token, "signature":signature, 'equipped':user_server['equip'], 'itemskey':user_server['items'].keys(), 'itemsvalue':user_server['items'].values(),
                                 'missionskey':user_server['missions'].keys(), 'missionsvalue':user_server['missions'].values(), 'coordinate':list(user_server['coordinate'])}
            else:
                Log.info("user %s login with wrong password" % user_name)
                tokenMessage = {"token": "", "signature": "", 'equipped':[], 'items':{}, 'missions':{}, 'coordinate':[]}
            return token_message
        except:
            Log.warn('login security check failed, traceback: %s' % traceback.format_exc())



        try:
            if self.__loginThreadLock.acquire():
                self.__tokenDict[token] = user_name
                print  "input  **********" + token
                self.__userMsgQueue[token] = Queue.Queue()
                # queue(maxsize = 0) : queue 队列无限大
                self.__loginThreadLock.release()
        except:
            Log.error("userinfo info failure")
            if self.__loginThreadLock.acquire():
                del self.__userMsgQueue[token]
                del self.__tokenDict[token]
                self.__loginThreadLock.release()
        try:
            userthread = threading.Thread(target=self.UserThread, args=(token,))
            userthread.start()
        except:
            Log.error("Error: unable to start thread for %s" % user_name)



    def LoginHandeler(self, CheckPassword, error):
        class Handler(SocketServer.StreamRequestHandler):
            """
            The request handler class for our server.

            It is instantiated once per connection to the server, and must
            override the handle() method to implement communication to the
            client.
            """
            def handle(self):
                #self.request is the TCP socket connected to the client
                
                try:
                    message = self.rfile.readline()
                    if message:
                        print "{} wrote:".format(self.client_address[0])
                        tokenMessage = CheckPassword(message)
                        print tokenMessage
                        print json.dumps(tokenMessage)
                        self.request.sendall(json.dumps(tokenMessage))
                    else:
                        raise Exception("client is off")  
                except :
                    error('login response failed, traceback: %s' % traceback.format_exc())

        return Handler
    def LoginServer(self):
        #在登陆进程中初始化相关的工具
        DataDriver.InitDB()
        Log.Init()
        self.__loginThreadLock = threading.Lock()
        try:
            loginServer = SocketServer.ThreadingTCPServer((LOGIN_HOST, LOGIN_PORT), self.LoginHandeler(self.CheckPassword, Log.error))

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
            loginServer.serve_forever()
        except :
            Log.error('port ERROR, traceback: %s' % traceback.format_exc())

    def UserThread(self, token):
        print "thread  init " + token
        que = self.__userMsgQueue.get(token)
        while que and not que.empty():
            msg = que.get()
            print str(msg)

    def ActionMsgDispatcher(self, msg):
        assert msg[u'token'] != u'' and msg[u'action'] != u''  "blank Action"
        try:
            token = base64.b64decode(msg[u'token'])
            token = SecTools.AESDecrypt(token)
            loginTime = token.rsplit(' ')[-1]
            action = msg[u'action']
        except:
            Log.info("wrong msg parsing ")
        if SecTools.EnHash(json.dumps(action) + loginTime) == base64.b64decode(msg[u'md5']):
            que = self.__userMsgQueue.get(token.encode('utf-8'))
            if que:
                 print que.qsize()
                 que.put(action)
            else:
                print "**********msg cannot put into queue because of token keyerror"

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
                HandlerUDPMessage(message)


                #socket = self.request[1]
                #print socket
                #print self.client_address
                #print "{} wrote:".format(self.client_address[0])
                #socket.sendto(json.dumps(response), self.client_address)

        return MyActionHandler

    def ActionServer(self):
        #HOST, PORT = "localhost", 9998
        actionServer = SocketServer.UDPServer((ACTION_HOST, ACTION_PORT), self.ActionHandler(self.ActionMsgDispatcher))
        actionServer.serve_forever()



if __name__ == "__main__":
    userset = Users()
    #userset.log = LoggerTools()
    #userset.sec = 
    LoginProcess = Process(target = userset.LoginServer)
    LoginProcess.start()
    ListenUDPProcess = Process(target = userset.ActionServer)
    ListenUDPProcess.start()

    

    

    