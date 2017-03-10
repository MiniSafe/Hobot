# coding:utf-8
import os
def work(msg,info):
    msg.content=msg.content.strip()
    if msg.content.startswith("exec"):
        if info.get('level', 3)<1:
            try:
                _,code=msg.content.split(' ',1)
                exec code
                return '代码执行完毕'
            except Exception,e:
                print e
                return help(info)
    else:
        return False
def help(info):
    if info.get('level',3)<1:
        return "#exec code 执行代码"
