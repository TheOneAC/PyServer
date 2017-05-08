#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Users(object):
    """所有玩家的集合,负责玩家登陆,同时实例化每一个玩家,放在列表中
    并接受每个玩家的请求,用多线程"""
    def __init__(self, *args, **kwargs):
        usrs = {}  #玩家集合
        return super(Users, self).__init__(*args, **kwargs)





class User(object):
    """一个玩家，包括玩家的物品，任务进度，位置，血量，装备等所有信息"""
