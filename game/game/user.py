#!/usr/bin/python
# -*- coding: UTF-8 -*-
class User(object):
    '''一个玩家，包括玩家的物品，任务进度，位置，血量，装备等所有信息'''
    def __init__(self, name, password):
    	
    	self.__name = name
    	self.__password = password
    	self.__blood_value = 10000
    	self.__position = ()
    	self.__mission = {}
    	self.__equipment = []
    	self.__drug = {}
    	self.__other_goods = {}


   
    def get_name(self):
        return self.__name
       
    def set_name(self, value):
        self.__name = value
    
    def get_password(self):
    	return self.__password




'''

if  __name__ == "__main__":
	
	user = User("hello", "12345")
	userName = user.get_name();
	print userName
'''