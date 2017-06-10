#!/usr/bin/python
# -*- coding: UTF-8 -*-
import configure
from pymongo import MongoClient
import pymongo

client = MongoClient(configure.DB_HOST, configure.DB_PORT)
db = client[configure.DB_NAME]
users = db[u'users']


users.remove({u'name':'zero'})
items = {u'2001':10, u'2002':10, u'3001':1, u'4001':1}
users.save({u'name':u'zero', u'password':u'4QrcOUm6Wau+VuBX8g+IPg==', u'equip':[3001], u'items':items, u'missions':{}, u'coordinate':(30,30)})
print users.index_information()
users.create_index([(u'name', pymongo.ASCENDING)])
print users.index_information()
