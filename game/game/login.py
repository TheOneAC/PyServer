#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time

import socket
import SocketServer
import logging, traceback  

import json, base64
import threading

from user import User
from configure import *
from log import LoggerTools as Log
from security import SecurityTools as SecTools
from data import DataDriver

class Login(object):
    """负责玩家登陆"""
    
    def __init__(self):
        pass

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
                token_message = {"token": "", "signature": "", 'equipped':[], 'itemskey':[], 'itemsvalue':[], 'missionskey':[], 'misionsvalue':[], 'coordinate':[]}
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
                try:
                    message = self.rfile.readline()
                    if message:
                        print "{} wrote:".format(self.client_address[0])
                        token_message = CheckPassword(message)
                        print token_message
                        self.request.sendall(json.dumps(token_message))
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

    

