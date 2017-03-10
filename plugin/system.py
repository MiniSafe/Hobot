# coding:utf-8
import os
def work(msg,info):
    msg=msg.content.strip()
    if msg.startswith("system"):
        level=info.get('level',3)
        if level<1:
            try:
                _,cmd=msg.split(' ',1)
                os.system(cmd)
                return '命令执行成功'
            except:
                return help(info)
        else:
            return False
    else:
        return False
def help(info):
    if info.get('level',3)<1:
        return "#system command 执行系统命令"