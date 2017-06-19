#!/usr/bin/python
# -*- coding: UTF-8 -*-
import random
import time
import math


def enum(**enums):
    return type('Enum', (object,), enums)


MONSTER_STATE = enum(RANDER=1, FOLLOW=2, DEATH=3)
MONSTER_TYPE = enum(BOSS=1, COMMON=2)


class SimpleMonster(object):
    def __init__(self,id=1,position=(1,2)):
        super(SimpleMonster, self).__init__()
        self.__id = id
        self.__position = position

    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, value):
        self.__id = value
    @id.deleter
    def id(self):
        del self.__id


    @property
    def position(self):
        return self.__position
    @position.setter
    def position(self, value):
        self.__position = value
    @position.deleter
    def position(self):
        del self.__position


    def __str__(self):
        list = {}
        list.setdefault('id', self.__id)
        list.setdefault('position', self.__position)

        return str(list)



class Monster(object):
    """怪,属性包括血量,位置等
    控制怪的行为：追踪，攻击，随机移动等"""



    def __init__(self, id=1, blood_value=100000, monster_type=MONSTER_TYPE.COMMON
                 , position=(1, 2), state=MONSTER_STATE.RANDER, attack_value=100, defense_value=10):
        super(Monster, self).__init__()
        self.__id = id
        self.__monster_type = monster_type
        self.__blood_value = blood_value
        self.__position = position
        self.__state = state
        self.__attack_value = attack_value
        self.__defense_value = defense_value



    def get_blood_by_tpye(self,monster_type):
        pass


    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, value):
        self.__id = value
    @id.deleter
    def id(self):
        del self.__id


    @property
    def position(self):
        return self.__position
    @position.setter
    def position(self, value):
        self.__position = value
    @position.deleter
    def position(self):
        del self.__position


    @property
    def blood_value(self):
        return self.__blood_value
    @blood_value.setter
    def blood_value(self, value):
        self.__blood_value = value
    @blood_value.deleter
    def blood_value(self):
        del self.__blood_value

    @property
    def state(self):
        return self.__state
    @state.setter
    def state(self, value):
        self.__state = value
    @state.deleter
    def state(self):
        del self.__state


    @property
    def attack_value(self):
        return self.__attack_value
    @attack_value.setter
    def attack_value(self, value):
        self.__attack_value = value
    @attack_value.deleter
    def attack_value(self):
        del self.__attack_value


    @property
    def defense_value(self):
        return self.__defense_value
    @defense_value.setter
    def defense_value(self, value):
        self.__defense_value = value
    @defense_value.deleter
    def defense_value(self):
        del self.__defense_value





    # 打印所有属性
    def __str__(self):
        list = {}
        list.setdefault('id', self.__id)
        list.setdefault('blood_value', self.__blood_value)
        list.setdefault('position', self.__position)
        list.setdefault('state', self.__state)
        list.setdefault('attack_value', self.__attack_value)
        list.setdefault('defense_value', self.__defense_value)
        return str(list)
