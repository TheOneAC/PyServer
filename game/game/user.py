#!/usr/bin/python
# -*- coding: UTF-8 -*-
import Queue
from data import DataDriver
from log import LoggerTools as Log
import threading
import  json, time
import configure



class User:
    '''一个玩家，包括玩家的物品，任务进度，位置，血量，装备等所有信息'''
    def __init__(self):
        self.__queue = Queue.Queue()
        self.__monster_queue = Queue.Queue()
        self.__name = u"zero"
        self.__password = None
        self.__position = ()
        self.__missions = {}
        self.__equip = []
        self.__items = {}
        self.token = u''
        self.sign = u''
        self.__login_time = u''
        self.__userthread = None
        self.__client_address = ()
        self.__socket = None
        
    def name():
        doc = u"用户名"
        def fget(self):
            return self.__name
        def fset(self, value):
            self.__name = value
        def fdel(self):
            del self.__name
        return locals()
    name = property(**name())

    def password():
        doc = u"密码"
        def fget(self):
            return self.__password
        def fset(self, value):
            self.__password = value
        def fdel(self):
            del self.__password
        return locals()
    password = property(**password())
    
    def position():
        doc = u"位置坐标"
        def fget(self):
            return self.__position
        def fset(self, value):
            self.__position = value
        def fdel(self):
            del self.__position
        return locals()
    position = property(**position())

    def missions():
        doc = u"任务."
        def fget(self):
            return self.__missions
        def fset(self, value):
            self.__missions = value
        def fdel(self):
            del self.__missions
        return locals()
    missions = property(**missions())

    def equip():
        doc = u"装备"
        def fget(self):
            return self.__equip
        def fset(self, value):
            self.__equip = value
        def fdel(self):
            del self.__equip
        return locals()
    equip = property(**equip())

    def items():
        doc = u"物品"
        def fget(self):
            return self.__items
        def fset(self, value):
            self.__items = value
        def fdel(self):
            del self.__items
        return locals()
    items = property(**items())

    def login_time():
        doc = u"登录时间"
        def fget(self):
            return self.__login_time
        def fset(self, value):
            self.__items = value
        def fdel(self):
            del self.__login_time
        return locals()
    login_time = property(**login_time())


    def userthread():
        doc = u"用户线程"
        def fget(self):
            return self.__userthread
        def fset(self, value):
            self.__userthread = value
        def fdel(self):
            del self.__userthread
        return locals()
    userthread = property(**userthread())

    #退出时存用户信息
    def DumpUserInfo(self,username):
        userinfo = {u'name':self.__name, u'password':self.__password,
                    u'equip':self.__equip, u'items':self.__items,
                    u'missions':self.__missions, u'coordinate':self.__position}
        DataDriver.DumpUserInfo(username, userinfo)

    def AddMonsterMsg(self, msg):
        self.__monster_queue.put(msg)

    #由action线程调用，添加msg
    def AddMsg(self, msg):
        self.__queue.put(msg)

    # 处理action，action由用户线程从msg里面取出来
    def ProcessAction(self, action,socket, client_address):
        if action[u'operate'] == "move": #玩家坐标
            self.__position = (action[u'para1'], action[u'para2'])
            action[u'operate'] = "position"
            #del action[u'sync']
            socket.sendto(json.dumps(action) , client_address)
            msg = {u'name': self.__name, u'action': action}
            self.__socket.sendto(json.dumps(msg), (configure.MONSTER_HOST, configure.MONSTER_PORT))
        elif action[u'operate'] == "add_item": #增加物品
            item_id = action[u'para1']
            if item_id in self.__items.keys():
                self.__items[item_id] += 1
            else:
                self.__items[item_id] = 1
            socket.sendto("True", client_address)
        elif action[u'operate'] == "remove_item": #减少物品
            item_id = action[u'para1']
            if item_id in self.__items.keys():
                if self.__items[item_id] == 1:
                    self.__items.pop(item_id)
                else:
                    self.__items[item_id] -= 1
            socket.sendto("True", client_address)
        elif action[u'operate'] == "equip": #穿脱装备
            item_id = action[u'para1']
            if not item_id in self.__items.keys():
                socket.sendto("False", client_address)
            else:
                item_id = int(item_id)
                #脱装备
                if item_id in self.__equip:
                    condition = lambda t: t != item_id
                    self.__equip = filter(condition, self.__equip)
                else: #穿装备
                    for i in xrange(len(self.__equip)):
                        if self.__equip[i] / 1000 == item_id / 1000:
                            if self.__equip[i] % 1000 != item_id % 1000:
                                self.__equip[i] = item_id
                            break
                    else:
                        self.__equip.append(item_id)
                print self.__equip;
                socket.sendto("True", client_address)
        elif action[u'operate'] == "mission": #更新任务
            mission_id = action[u'para1']
            if mission_id in self.__missions.keys():
                self.__missions[mission_id] += 1;
            else:
                self.__missions[mission_id] = 1;
            socket.sendto("True", client_address)
        elif action[u'operate'] == "init_hp":  # 获取初始血量
            socket.sendto(json.dumps(action), client_address)
        elif action[u'operate'] == "init_monster_position":# 获取怪物位置
            msg = {u'name': self.__name, u'action': action}
            self.__socket.sendto(json.dumps(msg), (configure.MONSTER_HOST, configure.MONSTER_PORT))


    def ProcessMosterAction(self, msg, client_address):
        print msg[u"monsteraction"]
        socket = msg[u'socket']
        for mon_position in msg[u"monsteraction"]:
            x = mon_position.get(u'x')
            y = mon_position.get(u'y')
            msg = {u'operate': "monster_position",u'para1':mon_position.get(u'monsterid'),u'para2':str(x) + ' ' + str(y)}
            socket.sendto(json.dumps(msg),self.__client_address )

    #读取自己的msg，并处理，同时负责定时存储
    def StartUser(self, token, AddLogoutUser):
        lasttime = time.time()
        while True:
            if not self.__monster_queue.empty():
                msg = self.__monster_queue.get()
                self.ProcessMosterAction(msg, self.__client_address)

            if time.time() % configure.DUMP_TIME_INTERVAL == 0:
                self.DumpUserInfo(token)
            if not self.__queue.empty():
                msg = self.__queue.get()
                lasttime = time.time()
                socket = msg[u'socket']
                client_address = msg[u'client_address']
                if not msg[u'action'] :
                    Log.debug(u'action不见了')
                    continue
                elif msg[u'action'][u'operate'] == "":
                    continue
                elif msg[u'action'][u'operate'] != "end":
                    print msg[u'action']
                    if msg[u'action'][u"sync"] != True:
                        self.__socket = socket
                        self.__client_address = client_address
                    del msg[u'action'][u"sync"]
                    self.ProcessAction(msg[u'action'], socket, client_address)
                else:
                    continue
            elif time.time() - lasttime > configure.TIMEOUT_SECONDS:
                break
        #用户信息写回数据库,并告诉主线程清理用户数据
        self.DumpUserInfo(token)
        AddLogoutUser(self.__name)

    #初始化用户线程，包括读取数据库，初始化话user对象，开用户线程
    def Init(self,token, client_address, AddLogoutUser):
        try:
            userinfo = DataDriver.GetUserInfo(token)
            logintime = DataDriver.GetLoginInfo(token)
        except:
            Log.error("Error: Get info for %s from DB failure" % token)
        try:
            self.__name = userinfo[u'name']
            self.__password = userinfo[u'password']
            self.__position = userinfo[u'coordinate']
            self.__missions = userinfo[u'missions']
            self.__equip = userinfo[u'equip']
            self.__items = userinfo[u'items']
            self.__login_time = logintime[u'logintime']
            self.__client_address = client_address
        except Exception as e:
            Log.error("Error: userinfo cached in server for %s failure" % token)
        try:
            userthread = threading.Thread(target=self.StartUser,args= (token,AddLogoutUser))
            #userthread.setDaemon(True)
            userthread.start()
            self.__userthread = userthread
        except:
            Log.error("Error: unable to start thread for %s" % token)

if __name__ == "__main__":
    user = User()
    user.Init("zero")
    print user.name


    



