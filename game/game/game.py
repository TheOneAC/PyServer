#!/usr/bin/python
# -*- coding: UTF-8 -*-

import users
import monster

class World(object):
    """世界类，负责与玩家线程交互，包含npc，怪物等所有玩家共享的全局信息"""
    def __init__(self):
        self.monsters = {}
        self.user = users.Users()