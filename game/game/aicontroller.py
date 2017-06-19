#!/usr/bin/python
# -*- coding: UTF-8 -*-
import random
import time
import user
import math
import monster

#TODO 消息的交互
class AIController(object):

    def __init__(self,monsters=[],users=[]):

        self.__monster_list = monsters
        self.__user_list = users
        self.ratio = 0.5



    def control(self):
        print 'begin'

        while True:

            for item in self.__monster_list:
                if item.state == monster.MONSTER_STATE.RANDER:
                    run_function = self.rander(item)
                    next(run_function)

                    print 'monster_id:',item.id,'position:',item.position
                    try:
                        run_function.send(random.uniform(0, 0.5))

                    except StopIteration:
                            print 'stop itertation'
                            continue



                elif item.state == monster.MONSTER_STATE.FOLLOW:
                    print('follow')
                    run_function = self.follow(item)
                    next(run_function)
                    try:
                        run_function.send(random.uniform(0, 0.5))

                    except StopIteration:
                        print 'follow stop iteration'
                        continue
                elif item.state == monster.MONSTER_STATE.DEATH:
                    self.death(item)
                    self.__monster_list.remove(item)




    # 漫走
    def rander(self,monster_item):

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
                if self.can_follow(monster_item,user_item):
                    monster_item.state =monster.MONSTER_STATE.FOLLOW
                    break
        sleep_cnt = yield monster_item.position
        print('let me think {0} secs'.format(sleep_cnt))
        time.sleep(sleep_cnt)

        return


    # 追随
    def follow(self,monster_item):
        print('follow')
        flag=False
        if self.__user_list is not None:
             for user_item in self.__user_list:
                 if self.can_follow(monster_item,user_item):
                    flag=True
                    monster_position = list(monster_item.position)
                    user_position = list(user_item.position)
                    monster_position[0]+=(user_position[0]-monster_position[0])*self.ratio
                    monster_position[1]+=(user_position[1]-monster_position[1])*self.ratio
                    monster_item.position = tuple(monster_position)
                    break
        if not flag:
           monster_item.state=monster.MONSTER_STATE.WALK


        if self.__user_list is not None:
            for user_item in self.__user_list:
                if self.can_attack(monster_item,user_item):
                    self.attack(monster_item,user_item)
                    break

        sleep_cnt = yield monster_item.position
        print('let me think {0} secs'.format(sleep_cnt))
        time.sleep(sleep_cnt)

        return



    # 攻击
    def attack(self,monster_item,user_item):
        print('attack')

        user_item.blood_value = user_item.blood_value-(monster_item.attack_value - user_item.defense_value)
        monster_item.blood_value = monster_item.blood_value -(user_item.attack_value - monster_item.defense_value)
        print 'monster_Id',monster_item.id,"blood:",monster_item.blood_value
        if monster_item.blood_value <= 0:
            monster_item.state = monster.MONSTER_STATE.DEATH

        return

    def can_attack(self,monster_item,user_item):
        monster_position = list(monster_item.position)
        user_position = list(user_item.position)

        distance = math.sqrt( (monster_position[0] - user_position[0]) * (monster_position[0] - user_position[0]) +
        (monster_position[1] - user_position[1]) * (monster_position[1] - user_position[1]) )

        if distance < 3:
            return True

        return False

    def can_follow(self,monster_item,user_item):
        monster_position = list(monster_item.position)
        user_position = list(user_item.position)

        distance = math.sqrt( (monster_position[0] - user_position[0]) * (monster_position[0] - user_position[0]) +
        (monster_position[1] - user_position[1]) * (monster_position[1] - user_position[1]) )

        if distance < 5:
            return True

        return False

    def death(self,monster_item):
        print 'monster_id',monster_item.id, "death"




