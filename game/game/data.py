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
        except Exception as e:
            Log.error('login security check failed,exception: %s traceback: %s' % (e, traceback.format_exc()))

    @classmethod #登陆时获取用户的所有信息
    def GetUserInfo(cls, user_name):
        try:
            users = cls.__db[u'users'] #确定集合
            tmp = users.find_one({u'name':user_name})
            if tmp == None:
                return None
            tmp.pop(u'_id')
            return tmp
        except Exception as e:
            Log.error('DataBase error, exception: %s traceback: %s' % (e, traceback.format_exc()))
            return None

    @classmethod  #把用户数据写回数据库
    def DumpUserInfo(cls,username, userinfo):
        try:
            users = cls.__db[u'users']  # 确定集合
            users.remove({u'name': username})
            users.save(userinfo)
            Log.info('Userinfo for %s dump into DB' % username)
        except Exception as e:
            Log.error('User Dump Error, exception: %s traceback: %s' % (e, traceback.format_exc()))


    @classmethod #更新用户临时表数据，登陆时调用
    def UpdateLoginInfo(cls,user_name,logintime):
        try:
            login =  cls.__db[u'logintime']
            login.remove({u'name':user_name})
            login.save({u'name':user_name,u'logintime':logintime})
        except Exception as e:
            Log.error('DataBase error, exception: %s traceback: %s' % (e, traceback.format_exc()))

    @classmethod
    def GetLoginInfo(cls, user_name):
        try:
            logininfo = cls.__db[u'logintime'] #确定集合
            tmp = logininfo.find_one({u'name':user_name})
            if tmp == None:
                return None
            tmp.pop(u'_id')
            return tmp
        except Exception as e:
            Log.error('DataBase error, exception: %s traceback: %s' % (e, traceback.format_exc()))
            return None