# coding:utf-8
import socket
def work(msg,info):
    msg=msg.content.strip()
    if msg.startswith("pings"):
        if not info.get('level', 3) < 4:
            return False
        try:
            msg=msg.split(' ')[-1]
            addr=socket.gethostbyname(msg)
            return '地址:'+msg+'\n解析的IP为:'+addr
        except:
            return help(info)
    else:
        return False
def help(info):
    if not info.get('level',3) < 4:
        return False
    return "#pings e.com 说出来你可能不信，ping是禁词"