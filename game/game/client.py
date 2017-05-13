#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import sys
from multiprocessing import Process
import os
import json
import base64

def login():
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
	    
	    tokenID = received[u'tokenID']
	    b64_tokenID = base64.b64decode(tokenID)
	finally:
	    sock.close()
	

	print "Sent:     {}".format(encode_data)
	print "Received: {}".format(received)

	return b64_tokenID
		

if __name__ == "__main__":
	#Client_login = Process(target=login)
	#Client_login.start()
	#Client_login.join()
	tokenID = login()
	print "tokenID = name + login_time: {}".format(tokenID)
	print "login Success!"
	

