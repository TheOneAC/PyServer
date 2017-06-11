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

    def UpLoginInfo(self,user_name, logintime):
        DataDriver.UpdateLoginInfo(user_name, logintime)

    def GetToken(self, message):
        token_message = None
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
                nowtime = str(time.time())
                self.UpLoginInfo(user_name, nowtime)
                token = user_name + ' ' + nowtime
                token = token.encode('utf-8')
                en_token, signature = SecTools.Encrypt(token)
                token_message = {"token": en_token, "signature":signature, 'equipped':user_server['equip'], 'itemskey':user_server['items'].keys(), 'itemsvalue':user_server['items'].values(),
                                 'missionskey':user_server['missions'].keys(), 'missionsvalue':user_server['missions'].values(), 'coordinate':list(user_server['coordinate'])}
            else:
                Log.info("user %s login with wrong password" % user_name)
                token_message = {"token": "", "signature": "", 'equipped':[], 'itemskey':[], 'itemsvalue':[], 'missionskey':[], 'misionsvalue':[], 'coordinate':[]}
        except:
            Log.warn('login security check failed, traceback: %s' % traceback.format_exc())
        finally:
            return token_message





    def LoginHandeler(self, GetToken, error):
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
                        token_message = GetToken(message)
                        print token_message
                        self.request.sendall(json.dumps(token_message))
                    else:
                        raise Exception("client is off")
                except :
                    error('login response failed, traceback: %s' % traceback.format_exc())

        return Handler
    def LoginServer(self):
        #在登陆进程中初始化相关的工具
        Log.Init()
        DataDriver.InitDB()
        self.__loginThreadLock = threading.Lock()
        try:
            loginServer = SocketServer.ThreadingTCPServer((LOGIN_HOST, LOGIN_PORT), self.LoginHandeler(self.GetToken, Log.error))

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
            loginServer.serve_forever()
        except :
            Log.error('port ERROR, traceback: %s' % traceback.format_exc())

    

