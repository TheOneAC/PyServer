#!/usr/bin/python
# -*- coding: UTF-8 -*-
import configure
from pymongo import MongoClient

client = MongoClient(configure.DB_HOST, configure.DB_PORT)
db = client[configure.DB_NAME]
users = db['users']

items = {u'2001':10, u'2002':10, u'4002':1}
users.insert({u'name':u'zero', u'password':u'4QrcOUm6Wau+VuBX8g+IPg==', u'equip':[3001], u'items':items, u'missions':{}, u'coordinate':(30,30)})

