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
from security import SecurityTools


class Users(object):
    """所有玩家的集合,负责玩家登陆,同时实例化每一个玩家,放在列表中
    并接受每个玩家的请求,用多程"""
    
    def __init__(self):
        self.__sec = SecurityTools()
        user = User()
        user.userName = "zero"
        rawPassword = '123456'
        #user.password = "4QrcOUm6Wau+VuBX8g+IPg=="
        user.password = base64.b64encode(self.__sec.EnHash(rawPassword + salt))
        self.__user = {
            user.userName: user
        }
        self.__tokenDict = {}
        self.__userMsgQueue = {}
    
    def sec():
        doc = "The __sec property."
        def fget(self):
            return self.__sec
        def fset(self, value):
            self.__sec = value
        def fdel(self):
            del self.__sec
        return locals()
    sec = property(**sec())
    

    def GetUser(self, userName):
        return self.__user[userName]

    def ActionMsgDispatcher(self, msg):
        print msg
        #token = base64.b64decode(msg[u'token'])
        #token = self.__AESDecrypt(token)
       # print  "token"+token
        #loginTime = token.rsplit(' ')[-1]
        #print loginTime
        #if self.__sec.EnHash(str( msg[u'action']) + loginTime) == base64.b64decode(msg[u'md5']):
            #self.__userMsgQueue[token].
        
        #while True: 
        #    while (not self.__userMsgQueue[token].empty()):





        return "HandlerUDPMessage"

    def CheckPassword(self, message):
        tokenMessage = None
        try:
            decode_message = json.loads(message)
            #print decode_message
            assert decode_message[u'name'] != u'' and decode_message[u'password'] != u''  "filed"
        except:
            Log.info('login decode failed')
            
        try:    
            #if True:
            if self.GetUser(decode_message[u'name']).password == decode_message[u'password']:
                Log.info("new user: %s login success" % decode_message[u'name'])
                userName = decode_message[u'name']
                token = userName + ' ' + str(time.time())
                token = token.encode('utf-8')
                token,signature = self.__sec.Encrypt(token)
                tokenMessage = {"token": token, "signature":signature}


            else:
                Log.info("user %s login with wrong password" % userName)
                tokenMessage = {"token": "", "signature": ""}
        except:
            Log.warn('login security check failed, traceback: %s' % traceback.format_exc())
        try:
            if self.__loginThreadLock.acquire():
                self.__tokenDict[token] = userName
                self.__userMsgQueue[token] = Queue.Queue()
                self.__loginThreadLock.release()
        except:
            Log.error("userinfo info failure")
            if self.__loginThreadLock.acquire():
                del self.__userMsgQueue[token]
                del self.__tokenDict[token]
                self.__loginThreadLock.release()
        finally:    
            return tokenMessage
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
                    message = self.request.recv(MESSAGE_SIZE)
                    if message:
                        print "{} wrote:".format(self.client_address[0])
                        
                        
                        tokenMessage = CheckPassword(message)
                        #print tokenMessage
                        self.request.sendall(json.dumps(tokenMessage))
                    else:
                        raise Exception("client is off")  
                except :
                    error('login response failed, traceback: %s' % traceback.format_exc())

        return Handler
    def LoginServer(self):
        #HOST, PORT = "0.0.0.0", 9999
        self.__loginThreadLock = threading.Lock()
        Log.Init()
        # Create the server, binding to localhost on port 9999
        try:
            loginServer = SocketServer.ThreadingTCPServer((LOGIN_HOST, LOGIN_PORT), self.LoginHandeler(self.CheckPassword, Log.error))

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
            loginServer.serve_forever()
        except :
            Log.error('port ERROR, traceback: %s' % traceback.format_exc())


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
                message = json.dumps(data)
                response = HandlerUDPMessage(message)
                socket = self.request[1]
                print socket
                print "{} wrote:".format(self.client_address[0])
                print response
                socket.sendto(json.dumps(response), self.client_address)

        return MyActionHandler

    def ActionServer(self):
        #HOST, PORT = "localhost", 9998
        actionServer = SocketServer.UDPServer((ACTION_HOST, ACTION_PORT), self.ActionHandler(self.ActionMsgDispatcher))
        actionServer.serve_forever()



if __name__ == "__main__":
    userset = Users()
    #userset.log = LoggerTools()
    #userset.sec = 
    LoginProcess = Process(target=userset.LoginServer)
    LoginProcess.start()
    ListenUDPProcess = Process(target=userset.ActionServer)
    ListenUDPProcess.start()

    

    

    