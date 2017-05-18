#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import sys
from multiprocessing import Process
import os
import json
import base64
import time
import logging
import traceback 


import configure
import security
from security import SecurityTools
def CheckTokenID(msg):
	print msg
	tokenID = ""
	try:
		tokenID = base64.b64decode(msg[u'token'])
		print msg[u'signature']
		sign = base64.b64decode(msg[u'signature'])
		print "tokenID:******" + tokenID
		print "sign:*******" + sign
		sec = SecurityTools()
		sha = sec.ENSHA(tokenID)
		de_sign = sec.PublicVerify(sign)
		if sha != de_sign:
			raise Exception("SIGN VERIFY ERROR")
		else:

			tokenID = sec.AESDecrypt(tokenID) 
			#print "tokenID+++" + tokenID
	except:
		logging.warning('tokenID checkout failed, traceback: %s' % traceback.format_exc()) 
	finally:
		return tokenID

def Login():
	HOST, PORT = "localhost", 9999
	data = {"name":"zero","password":"123456"}
	encode_data = json.dumps(data)

	# Create a socket (SOCK_STREAM means a TCP socket)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tokenID = ""
	try:
	    # Connect to server and send data
	    sock.connect((HOST, PORT))
	    sock.sendall(encode_data + "\n")

	    # Receive data from the server and shut down
	    received = sock.recv(1024)
	    #
	    received = json.loads(received)
	    #b64_received = base64.b64decode(received)
	    #print type(received)
	    tokenID = CheckTokenID(received)
	    
	except:
		logging.warning('login response failed, traceback: %s' % traceback.format_exc()) 

	finally:
	    sock.close()
	

	#print "Sent:     {}".format(encode_data)
	#print "Received: {}".format(received)

	return tokenID

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
	

