#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import threading
import time

import SocketServer
from multiprocessing import Process
import os
import json


class users():
	def __init__(self):
		self.__user = {}
	

	def HandlerMessage(self, message):
		pass

	def CheckPassword(self, decode_message):
		print "yes!"
		token_message = ""
		if True:
			token_message = {"tokenID": decode_message[u'name'] + str(time.time())}
		return token_message
	def Handeler(self, CheckPassword):
		class MyTCPHandler(SocketServer.BaseRequestHandler):
			"""
			The request handler class for our server.

			It is instantiated once per connection to the server, and must
			override the handle() method to implement communication to the
			client.
			"""

			def handle(self):
				# self.request is the TCP socket connected to the client
				
				message = self.request.recv(1024)
				decode_message = json.loads(message)
				print "{} wrote:".format(self.client_address[0])
				print decode_message

				#check id and password , create tokenID
				token_message = CheckPassword(decode_message)
				self.request.sendall(json.dumps(token_message))
		return MyTCPHandler
	def MyTCPServer(self):
		HOST, PORT = "localhost", 9999

		# Create the server, binding to localhost on port 9999
		server = SocketServer.TCPServer((HOST, PORT), self.Handeler(self.CheckPassword))
		# Activate the server; this will keep running until you
		# interrupt the program with Ctrl-C
		server.serve_forever()





if __name__ == "__main__":
	userset = users()
	TCPProcess = Process(target=userset.MyTCPServer)
	TCPProcess.start()
	
    

	

	