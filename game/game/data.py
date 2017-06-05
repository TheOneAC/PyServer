#!/usr/bin/python
# -*- coding: UTF-8 -*-
from pymongo import MongoClient
import log
import configure

class DataDriver:
    """数据库操作类"""
    __db = None

    @classmethod #初始化数据库
    def InitDB(cls):
        try:
            client = MongoClient(configure.DB_HOST, configure.DB_PORT)
            cls.__db = client[configure.DB_NAME]
        except:
            Log.error("DB connection failed")

    @classmethod #登陆时获取用户的所有信息
    def GetUserInfo(cls, user_name):
        users = cls.__db[u'users'] #确定集合
        tmp = users.find_one({u'name':user_name})
        tmp.pop('_id')
        return tmp
      