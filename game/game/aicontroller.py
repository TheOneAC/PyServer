#!/usr/bin/python
# -*- coding: UTF-8 -*-
import SocketServer
import random
import time
import user
import math
from monster import *
import configure as config
import socket
import json
import threading
from Queue import Queue

'''
json格式:
接收 action
发送 monsteraction
name : user_id
action/monsteraction :{

operater : move/hit
para1 : x / monster_id
para2 : y / attack_value

}

'''
class UserInfo(object):
    def __init__(self):
        self.name = ""
        self.position = (-1,-1)


#TODO 消息的交互
class AIController(object):
    def __init__(self):
        pass

    def Control(self):
        print 'begin'

        while True:
            if not self.__msg_queue.empty():
                pass
            for item in self.__monster_list:
                if item.state == MONSTER_STATE.RANDER:
                    run_function = self.Wander(item)
                    next(run_function)

                    print 'monster_id:',item.id,'position:',item.position
                    try:
                        run_function.send(random.uniform(0, 0.5))

                    except StopIteration:
                        print 'stop itertation'
                        continue
                elif item.state == MONSTER_STATE.FOLLOW:
                    print('follow')
                    run_function = self.Follow(item)
                    next(run_function)
                    try:
                        run_function.send(random.uniform(0, 0.5))

                    except StopIteration:
                        print 'follow stop iteration'
                        continue
                elif item.state == MONSTER_STATE.DEATH:
                    self.Death(item)
                    self.__monster_list.remove(item)




    # 漫走
    def Wander(self,monster_item):

        print('rander')

        temp = list(monster_item.position)
        x = random.randint(-1, 1)
        y = random.randint(-1, 1)
        temp[0] += x
        temp[1] += y
        if temp[0] < 0:
            temp[0] = 0
        if temp[1] < 0:
            temp[1] = 0

        monster_item.position = tuple(temp)

        if self.__user_list is not None:
            for user_item in self.__user_list:
                if self.__CanFollow(monster_item,user_item):
                    monster_item.state = MONSTER_STATE.FOLLOW
                    break
        sleep_cnt = yield monster_item.position
        print('let me think {0} secs'.format(sleep_cnt))
        time.sleep(sleep_cnt)

        return


    # 追随
    def Follow(self,monster_item):
        print('follow')
        flag = False
        if self.__user_list is not None:
             for user_item in self.__user_list:
                 if self.__CanFollow(monster_item,user_item):
                    flag=True
                    monster_position = list(monster_item.position)
                    user_position = list(user_item.position)
                    monster_position[0] += (user_position[0]-monster_position[0])*self.ratio
                    monster_position[1] += (user_position[1]-monster_position[1])*self.ratio
                    monster_item.position = tuple(monster_position)
                    break
        if not flag:
           monster_item.state= MONSTER_STATE.WALK


        if self.__user_list is not None:
            for user_item in self.__user_list:
                if self.__CanAttack(monster_item,user_item):
                    self.Attack(monster_item,user_item)
                    break

        sleep_cnt = yield monster_item.position
        print('let me think {0} secs'.format(sleep_cnt))
        time.sleep(sleep_cnt)

        return



    # 攻击
    def Attack(self, monster_item, user_item):
        print('attack')

        user_item.blood_value = user_item.blood_value-(monster_item.attack_value - user_item.defense_value)
        monster_item.blood_value = monster_item.blood_value -(user_item.attack_value - monster_item.defense_value)
        print 'monster_Id',monster_item.id,"blood:",monster_item.blood_value
        if monster_item.blood_value <= 0:
            monster_item.state = MONSTER_STATE.DEATH

        return

    def __CanAttack(self, monster_item, user_item):
        monster_position = list(monster_item.position)
        user_position = list(user_item.position)

        distance = math.sqrt( (monster_position[0] - user_position[0]) * (monster_position[0] - user_position[0]) +
        (monster_position[1] - user_position[1]) * (monster_position[1] - user_position[1]) )

        if distance < 3:
            return True

        return False

    def __CanFollow(self, monster_item, user_item):
        monster_position = list(monster_item.position)
        user_position = list(user_item.position)

        distance = math.sqrt( (monster_position[0] - user_position[0]) * (monster_position[0] - user_position[0]) +
        (monster_position[1] - user_position[1]) * (monster_position[1] - user_position[1]) )

        if distance < 5:
            return True

        return False

    def Death(self,monster_item):
        print 'monster_id',monster_item.id, "death"

    def InitMonster(self):
        random.seed(time.time())
        for i in range(99):
            mon = Monster(id=i+1,position=(random.randint(0,2147483647) % 500, random.randint(0,2147483647) % 500) )
            self.__monster_list.append(mon)
        self.__monster_list.append(self.__boss)





    def UpdateUdpMessage(self, msg, socket, client_address):
        #保存action server的地址
        self.__client_address = client_address
        self.__socket = socket

        msg = json.loads(msg)
        user_action = msg[u"action"][u"operate"]
        if user_action == "move":
            pass
        elif user_action == "hit":
            pass
        elif user_action == "init_monster_position":
            #response = {u"name":msg[u"name"],u"monsteraction":[]}
            monsterInfo = []
            for info in self.__monster_list:
                simple_mon = {}
                simple_mon[u"monsterid"] = info.id
                simple_mon[u"x"] = info.position[0]
                simple_mon[u"y"] = info.position[1]
                print("x,y:", info.position[0],info.position[1])
                monsterInfo.append(simple_mon)

            response = {u"name":msg[u"name"],u"monsteraction":monsterInfo}
            print client_address
            print len(monsterInfo)
            #print json.dumps(response)
            socket.sendto(json.dumps(response), client_address)



    def UpdateHandler(self, UpdateUdpMessage):
        class MyUpdateHandler(SocketServer.BaseRequestHandler):
            def handle(self):
                data = self.request[0].strip()
                socket = self.request[1]
                UpdateUdpMessage(data, socket, self.client_address)
        return MyUpdateHandler

    def StartAIServer(self):
        self.__boss = Monster(id = 0, blood_value = config.BOSS_HP, monster_type = MONSTER_TYPE.BOSS, position = (20,20), state = MONSTER_STATE.WANDER, attack_value = 1000, defense_value = 1000)
        self.__monster_list = []
        self.__user_list = [] #UserInfo
        self.__msg_queue = Queue()
        self.ratio = 0.5
        self.InitMonster()
        return SocketServer.UDPServer((config.MONSTER_HOST, config.MONSTER_PORT), self.UpdateHandler(self.UpdateUdpMessage))


    def StartAI(self):
        server = self.StartAIServer()
        server.serve_forever()
        #processer = threading.Thread(target = self.Control, args = ())
        #userthread.setDaemon(True)
        #processer.start()


if __name__ == "__main__":

    controller = AIController()
    controller.StartAI()