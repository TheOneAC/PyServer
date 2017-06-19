#!/usr/bin/python
# -*- coding: utf-8 -*-


DB_HOST, DB_PORT = "219.219.220.109", 9997
LOGIN_HOST, LOGIN_PORT = "0.0.0.0", 9999
ACTION_HOST, ACTION_PORT = "0.0.0.0", 9998
MESSAGE_SIZE = 10240

DB_NAME = "game"
DB_USERNAME = "xyd"
DB_USERPASSWORD = "ffffffff"

logFileName = 'log/logfile.txt'

publicKey = 'secret/public'
privateKey = 'secret/private'
enKey = "68b329da9893e340"
salt = ""

TIMEOUT_SECONDS = 3  #用户心跳信息接收的超时阈值
DUMP_TIME_INTERVAL = 100 #用户信息写回数据库的时间间隔

MOSTER_HOST, MONSTER_PORT = "211.86.158.157",9996
