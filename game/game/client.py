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
def Checktoken(msg):
    #print "received msg " + msg
    token = None
    try:
        #print "base3284290385405************************" +msg[u'token']

        token = base64.b64decode(msg[u'token'])
        if token == "":
            return token
        #assert message[u'token'] != u'' and message[u'signature'] != u''  "filed"
        signature = base64.b64decode(msg[u'signature'])
        sec = SecurityTools()
        verify = sec.Verify(token, signature)
        if not verify:
            raise Exception("signature VERIFY ERROR")
        else:
            token = sec.AESDecrypt(token)
    except:
        logging.warning('token checkout failed, traceback: %s' % traceback.format_exc()) 
    finally:
        return token

def Login():
    HOST, PORT = "localhost", 9999
    #data = {"name":"zero","password":"123456"}
    #encode_data = json.dumps(data)
    sec = SecurityTools()
    encode_data = sec.LoginEncrypt("one","123456")

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    token = ""
    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(encode_data+ "\n")
        #print "send sucess"
        # Receive data from the server and shut down
        received = sock.recv(1024)
        #
        received = json.loads(received)
        print received
        #b64_received = base64.b64decode(received)
        #print type(received)
        token = Checktoken(received)
        
    except:
        logging.warning('login response failed, traceback: %s' % traceback.format_exc()) 

    finally:
        sock.close()
    

    #print "Sent:     {}".format(encode_data)
    #print "Received: {}".format(received)

    return token

def Actionmsg(token):
    monsterID = "monster100"
    action = {
        u"operate" : u"hit",
        u"para1": u'',
        u"para2": u""
    }
    username = token.split(' ')[0]
    loginTime = token.rsplit(' ')[-1]
    #print username
    sec = SecurityTools()
    #AESToken = sec.AESEncrypt(token)
    tomd5 = action["operate"] + action['para1'] + action['para2'] + loginTime
    print base64.b64encode(sec.EnHash(tomd5))
    #print msg[u'md5']
    md5str = sec.EnHash(str(tomd5))
    msgFmt = {"name": username, "md5": base64.b64encode(md5str), "action":action }
    return msgFmt


def ActionClient(token):
    HOST, PORT = "127.0.0.1", 9998
    

    # SOCK_DGRAM is the socket type to use for UDP sockets
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # As you can see, there is no connect() call; UDP has no connections.
    # Instead, data is directly sent to the recipient via sendto().
    msg = Actionmsg(token)

    print msg

    msg = json.dumps(msg) 
    sock.sendto(msg, (HOST, PORT))
    received = sock.recv(1024)
    print "Received: {}".format(received)


if __name__ == "__main__":
    #Client_login = Process(target=login)
    #Client_login.start()
    #Client_login.join()
    token = Login()
    print "token = name + login_time: {}".format(token)
    
    if token:
        print "login Success!"
        ActionClient(token)
    else:
        print "login failure, maybe wrong password"

