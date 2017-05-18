#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time

import socket
import SocketServer
from multiprocessing import Process
import logging
import traceback  

import json
import  base64


from user import User
from configure import *

from security import SecurityTools

class users(object):
	"""所有玩家的集合,负责玩家登陆,同时实例化每一个玩家,放在列表中
    并接受每个玩家的请求,用多程"""
    
	def __init__(self):
		self.__user = {
			"zero":User("zero", "123456"),
			"hello":User("hello", "123456")
		}
		self.sec = SecurityTools()
	def GetUser(self, name):
		return self.__user[name]

	def HandlerActionMessage(self, message):
		print message

		return "HandlerUDPMessage"

	def CheckPassword(self, decode_message):
		
		tokenMessage = ""
		try:
			#if True:
			if self.GetUser(decode_message['name']).get_password() == decode_message['password']:
				tokenID = decode_message[u'name'] + decode_message['password']+ str(time.time())
				enTokenID,sign = self.sec.Encrypt(tokenID)
				#b64_tokenID = 
				#sign = self.sec.Encrypt(tokenID)
				#b64_sign = base64.b64encode(sign)
				tokenMessage = {"token": base64.b64encode(enTokenID), "signature":base64.b64encode(sign)}
				print  tokenMessage
				#tokenMessage = {"tokenID": enTokenID, "sign":sign}
		except:
			logging.warning('login security check failed, traceback: %s' % traceback.format_exc())
		finally:	
			return tokenMessage
	def LoginHandeler(self, CheckPassword):
		class MyTCPHandler(SocketServer.BaseRequestHandler):
			"""
			The request handler class for our server.

			It is instantiated once per connection to the server, and must
			override the handle() method to implement communication to the
			client.
			"""

			def handle(self):
				# self.request is the TCP socket connected to the client
				logging.info("new user conect")
				try:
					message = self.request.recv(MESSAGE_SIZE)
					if message:
						decode_message = json.loads(message)
						print "{} wrote:".format(self.client_address[0])
						print decode_message
						#check id and password , create tokenID
						tokenMessage = CheckPassword(decode_message)

						self.request.sendall(json.dumps(tokenMessage))
					else:
						raise Exception("client is off")  
				except :
					logging.warning('login response failed, traceback: %s' % traceback.format_exc())

		return MyTCPHandler
	def LoginServer(self):
		#HOST, PORT = "0.0.0.0", 9999

		# Create the server, binding to localhost on port 9999
		loginServer = SocketServer.TCPServer((LOGIN_HOST, LOGIN_PORT), self.LoginHandeler(self.CheckPassword))
		# Activate the server; this will keep running until you
		# interrupt the program with Ctrl-C
		loginServer.serve_forever()


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
	LoginProcess = Process(target=userset.LoginServer)
	LoginProcess.start()
	ListenUDPProcess = Process(target=userset.ActionServer)
	ListenUDPProcess.start()
    

	

	