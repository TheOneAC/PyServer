#!/usr/bin/python
# -*- coding: UTF-8 -*-
from pymongo import MongoClient

class DataDriver:
    """数据库操作类"""

    @classmethod
    def ReadPasswd(cls, user_name):
        
