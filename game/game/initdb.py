#!/usr/bin/python
# -*- coding: UTF-8 -*-
import configure
from pymongo import MongoClient

client = MongoClient(configure.DB_HOST, configure.DB_PORT)
db = client[configure.DB_NAME]
users = db['users']

items = {'2001':10, '2002':10, '4002':1}
users.insert({'name':'zero', 'password':'4QrcOUm6Wau+VuBX8g+IPg==', 'equip':[3001], 'items':items, 'missions':{}, 'coordinate':(30,30)})

