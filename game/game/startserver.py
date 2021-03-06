#!/usr/bin/python
# -*- coding: utf-8 -*-

from multiprocessing import Process
from login import Login
from action import Action
from aicontroller import AIController

if __name__ == '__main__':
    #打开登录服务器
    login = Login()
    login_process = Process(target = login.LoginServer)
    login_process.start()

    #enemy = AIController()
    #enemy_process = Process(target = enemy.StartAI)
    #enemy_process.start()

    actions = Action()
    listen_udp_process = Process(target = actions.ActionServer)
    listen_udp_process.start()
