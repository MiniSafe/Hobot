#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import imp
import  json
import urllib2
import socket
import threading
import json
from qqbot import QQBot
import time

modules=[]
# 获取机器人接口的返回文本
def getAI(text):
    aa = urllib2.urlopen(
        "http://www.tuling123.com/openapi/api?key="+图灵机器人apikey+"&info=" + text).read()
    return json.loads(aa).get('text','机器人出错了..')

# 获取插件帮助信息
def helpinfo(infomation):
    global modules
    result = []
    for module in modules:
        info = ""
        try:
            info = module.help(infomation)
        except Exception, e:
            print e
        if info:
            result.append(info)
    return '\n'.join(result)

def load_module():
    global modules
    modules = []
    for plugin in os.listdir('plugin/'):
        plugin = plugin.split('.')
        print plugin
        if plugin[-1] != 'py':
            continue
        try:
            module = imp.new_module('.'.join(plugin[:-1]))
            exec open('plugin/' + '.'.join(plugin)).read() in module.__dict__
            modules.append(module)
        except Exception, e:
            print e


def work(msg,infomation):
    global modules
    for module in modules:
        info = ""
        try:
            info = module.work(msg,infomation)
        except Exception, e:
            print e
        if info:
            msg.Reply(info)
            break


load_module()
if not os.path.exists('users/'):
    os.makedirs('users/')

myqqbot = QQBot(qq=你要登陆的QQ)
mapping={}


@myqqbot.On('qqmessage')
def handler(bot, msg):
    global blackList
    global mapping
    msg.content=msg.content.strip(' ')
    qq=''
    if msg.contact.ctype == 'buddy':
        qq=str(msg.contact.qq)
    else:
        qq=mapping.get(str(msg.memberUin), None)
    if not qq:
        mapping[str(msg.memberUin)]=myqqbot.uin2qq(msg.memberUin)
        qq=mapping.get(str(msg.memberUin))
    print '用户QQ:',qq,'uin:',msg.memberUin
    infomation = {}
    if os.path.exists('users/' + str(qq) + ".ini"):
        try:
            infomation = json.loads(open('users/' + str(qq) + ".ini").read())
        except:
            pass
    if qq == '1197795981' and msg.content.startswith('#'):
        infomation['level'] = 0
        if msg.content == "#test" and msg.contact.ctype != 'buddy':
            print msg.contact.uin, myqqbot.uin2qq(msg.contact.uin), msg.memberUin, myqqbot.uin2qq(msg.memberUin)
            for x in msg.contact.members:
                print x, msg.contact.members[x], myqqbot.uin2qq(x)
        if msg.content == "#stop":
            bot.Stop()
        if msg.content == "#reload_module":
            load_module()
            msg.Reply("模块已重新加载")
            return
    if msg.content.startswith("#help"):
        if not msg.content=='#help':
            try:
                infomation['level']=int(msg.content.strip().split()[1])
            except:
                return
        info = '本机器人功能使用格式为:#功能 [参数1 参数2 ...] 解释\n功能列表:'
        msg.Reply(info)
        msg.Reply(helpinfo(infomation))
        return

    if msg.content.startswith("#"):
        bad = ['baidu.com', 'google.com', 'gov', 'edu','jd.com','fbi.gov','127.0.0.1','tencent'] #屏蔽名单
        if infomation.get('level', 3) < 2: # 如果level是小于二级是没有黑名单的
            pass
        elif True in [True if x in msg.content.lower() else False for x in bad]:
            if qq!='':
                msg.content = 'token set '+qq+' 4' # 直接修改用户命令，并且下一条修改临时用户权限，做到自动修改等级为4
                infomation={'level':0}
                threading.Thread(target=work, args=(msg, infomation)).start()
            msg.Reply('恭喜这位用户踩雷，黑名单有请')
            return
        msg.content = msg.content[1:]
        threading.Thread(target=work, args=(msg,infomation)).start()
        return
    if msg.contact.ctype == 'buddy':  #只有私聊回复
        msg.Reply(getAI(msg.content))

myqqbot.Login()
myqqbot.Run()
