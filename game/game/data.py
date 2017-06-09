#!/usr/bin/python
# -*- coding: UTF-8 -*-
from pymongo import MongoClient
from log import LoggerTools as Log
import configure
import traceback

class DataDriver:
    """数据库操作类"""
    __db = None

    @classmethod #初始化数据库
    def InitDB(cls):
        try:
            client = MongoClient(configure.DB_HOST, configure.DB_PORT)
            cls.__db = client[configure.DB_NAME]
            cls.__db.authenticate(configure.DB_USERNAME, configure.DB_USERPASSWORD)
        except:
            Log.error("DB connection failed")

    @classmethod #登陆时获取用户的所有信息
    def GetUserInfo(cls, user_name):
        try:
            users = cls.__db[u'users'] #确定集合
            tmp = users.find_one({u'name':user_name})
            if tmp == None:
                return None
            tmp.pop('_id')
            return tmp
        except:
            Log.error('DataBase error: %s' % traceback.format_exc())
            return None
    def GetUserInfo(cls, user_name):
        try:
            users = cls.__db[u'logintime'] #确定集合
            tmp = users.find_one({u'name':user_name})
            if tmp == None:
                return None
            tmp.pop('_id')
            return tmp
        except:
            Log.error('DataBase error: %s' % traceback.format_exc())
            return None
      