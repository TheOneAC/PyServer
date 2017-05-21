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
from log import LoggerTools
from security import SecurityTools

class users(object):
	"""所有玩家的集合,负责玩家登陆,同时实例化每一个玩家,放在列表中
    并接受每个玩家的请求,用多程"""
    
	def __init__(self):
		
		self.__userMsgQueue = {}
		self.__log = LoggerTools()
		self.__log.Init()
		self.__sec = SecurityTools()
		user = User()
		user.userName = "zero"
		user.password = self.__sec.EnHash("123456" + salt)
		self.__user = {
			user.userName: user
		}
	
	def log():
	    doc = "The __log property."
	    def fget(self):
	        return self.__log
	    def fset(self, value):
	        self.__log = value
	    def fdel(self):
	        del self.__log
	    return locals()
	log = property(**log())
	
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

	def HandlerActionMessage(self, message):
		#print message

		return "HandlerUDPMessage"

	def CheckPassword(self, message):
		
		tokenMessage = None
		try:
			message = base64.b64decode(message)
			message = self.__sec.AESDecrypt(message)
			#print message
			decode_message = json.loads(message)
			
		except:
			self.__log.info('login security decode failed')
		try:	
			#if True:
			if self.GetUser(decode_message[u'userName']).password == base64.b64decode(decode_message['password']):
				self.__log.info("new user: %s login success" % decode_message['userName'])

				tokenID = decode_message[u'userName'] + decode_message['password'] + str(time.time())
				token,signature = self.sec.Encrypt(tokenID)
				tokenMessage = {"token": base64.b64encode(token), "signature":base64.b64encode(signature)}
		except:
			self.__log.warn('login security check failed, traceback: %s' % traceback.format_exc())
		finally:	
			return tokenMessage
	def LoginHandeler(self, CheckPassword,error):
		class MyTCPHandler(SocketServer.BaseRequestHandler):
			"""
			The request handler class for our server.

			It is instantiated once per connection to the server, and must
			override the handle() method to implement communication to the
			client.
			"""

			def handle(self):
				# self.request is the TCP socket connected to the client
				
				try:
					message = self.request.recv(MESSAGE_SIZE)
					if message:
						print "{} wrote:".format(self.client_address[0])
						
						
						tokenMessage = CheckPassword(message)
						
						self.request.sendall(json.dumps(tokenMessage))
					else:
						raise Exception("client is off")  
				except :
					error('login response failed, traceback: %s' % traceback.format_exc())

		return MyTCPHandler
	def LoginServer(self):
		#HOST, PORT = "0.0.0.0", 9999

		# Create the server, binding to localhost on port 9999
		try:
			loginServer = SocketServer.TCPServer((LOGIN_HOST, LOGIN_PORT), self.LoginHandeler(self.CheckPassword, self.log.error))

		# Activate the server; this will keep running until you
		# interrupt the program with Ctrl-C
			loginServer.serve_forever()
		except :
			self.__log.error('port ERROR, traceback: %s' % traceback.format_exc())


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
		        print "{} wrote:".format(self.client_address[0])
		        print response
		        socket.sendto(json.dumps(response), self.client_address)

		return MyActionHandler

	def ActionServer(self):
		#HOST, PORT = "localhost", 9998
		actionServer = SocketServer.UDPServer((ACTION_HOST, ACTION_PORT), self.ActionHandler(self.HandlerActionMessage))
		actionServer.serve_forever()



if __name__ == "__main__":
	userset = users()
	#userset.log = LoggerTools()
	#userset.sec = 
	LoginProcess = Process(target=userset.LoginServer)
	LoginProcess.start()
	ListenUDPProcess = Process(target=userset.ActionServer)
	ListenUDPProcess.start()
    

	

	