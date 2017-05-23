#!/usr/bin/python
# -*- coding: UTF-8 -*-
class User():
    '''一个玩家，包括玩家的物品，任务进度，位置，血量，装备等所有信息'''
    def __init__(self):
        
        self.__name = "zero"
        self.__password = None
        self.__blood_value = 10000
        self.__position = ()
        self.__mission = {}
        self.__equipment = []
        self.__drug = {}
        self.__other_goods = {}

    def name():
        doc = "The __name property."
        def fget(self):
            return self.__name
        def fset(self, value):
            self.__name = value
        def fdel(self):
            del self.__name
        return locals()
    name = property(**name())

    def password():
        doc = "The __password property."
        def fget(self):
            return self.__password
        def fset(self, value):
            self.__password = value
        def fdel(self):
            del self.__password
        return locals()
    password = property(**password())

    
    def blood_value():
        doc = "The __blood_value property."
        def fget(self):
            return self.__blood_value
        def fset(self, value):
            self.__blood_value = value
        def fdel(self):
            del self.__blood_value
        return locals()
    blood_value = property(**blood_value())

    
    def position():
        doc = "The __position property."
        def fget(self):
            return self.__position
        def fset(self, value):
            self.__position = value
        def fdel(self):
            del self.__position
        return locals()
    position = property(**position())
    
    @classmethod
    def rename(self,newname):
        self.__name = newname

    
    
    

if __name__ == "__main__":
    user = User()
    
    print user.name
    user.rename("one")
    print user.name
    



