#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import sys
from multiprocessing import Process
import os
import json
import base64
import time

import configure
from aes import Decrypt

def Login():
	HOST, PORT = "localhost", 9999
	data = {"name":"zero","password":"123456"}
	encode_data = json.dumps(data)

	# Create a socket (SOCK_STREAM means a TCP socket)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	b64_tokenID = ""
	try:
	    # Connect to server and send data
	    sock.connect((HOST, PORT))
	    sock.sendall(encode_data + "\n")

	    # Receive data from the server and shut down
	    received = sock.recv(1024)
	    #b64_received = base64.b64decode(received)
	    received = json.loads(received)
	    #
	    #print type(received)
	    tokenID = received[u'tokenID']
	    decrypt_tokenID = Decrypt(tokenID)
	    

	finally:
	    sock.close()
	

	print "Sent:     {}".format(encode_data)
	print "Received: {}".format(received)

	return decrypt_tokenID

def UpdateUDPMessage(tokenID):
	monsterID = "monster100"
	behavior = {
		"target" : monsterID,
		"operator": "hit" # enum
		
	}
	message = {
		"tokenID":  tokenID,
		"time":     time.time(),
		"behavior": behavior
	}
	return message
		
def ActionClient(tokenID):
	HOST, PORT = "219.219.220.224", 9998
	

	# SOCK_DGRAM is the socket type to use for UDP sockets
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	# As you can see, there is no connect() call; UDP has no connections.
	# Instead, data is directly sent to the recipient via sendto().
	
	message = UpdateUDPMessage(tokenID)
	
	message = json.dumps(message) 
	sock.sendto(message + "\n", (HOST, PORT))
	received = sock.recv(1024)

	print "Sent:     {}".format(message)
	print "Received: {}".format(received)

if __name__ == "__main__":
	#Client_login = Process(target=login)
	#Client_login.start()
	#Client_login.join()
	tokenID = Login()
	print "tokenID = name + login_time: {}".format(tokenID)
	print "login Success!"
	if tokenID != "":
		ActionClient(tokenID)
	

