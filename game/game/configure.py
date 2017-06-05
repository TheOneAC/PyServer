#!/usr/bin/python
# -*- coding: utf-8 -*-


LOGIN_HOST, LOGIN_PORT = "0.0.0.0", 9999
ACTION_HOST, ACTION_PORT = "0.0.0.0", 9998
MESSAGE_SIZE = 10240
enKey = "68b329da9893e340"
salt = ""

logFileName = 'log/logfile.txt'

from M2Crypto import RSA
publicKey = 'secret/public'
privateKey = 'secret/private'
