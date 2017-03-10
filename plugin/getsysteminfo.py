#coding:utf-8
import os
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])
def work(msg,info):
    if msg.content != 'getsysteminfo':
        return False
    if not info.get('level',3) < 4:
        return False
    try:
        RAM_stats = getRAMinfo()
        DISK_stats = getDiskSpace()
        return "CPU温度:"+getCPUtemperature()+"℃\nCPU使用:"+getCPUuse()+\
              "%\nRAM总数:"+str(round(int(RAM_stats[0]) / 1000, 1)) + "MB\nRAM使用:"+str(round(int(RAM_stats[1]) / 1000, 1)) +\
               "MB\nRAM未用:"+str(round(int(RAM_stats[2]) / 1000, 1)) + "MB\n磁盘总数:"+DISK_stats[0]+\
               "\n磁盘使用:"+DISK_stats[1]+"\n磁盘空闲:"+DISK_stats[2]
    except Exception,e:
        return help()
        # return str(e)
def help(info):
    if not info.get('level',3) < 4:
        return False
    return "#getsysteminfo 获取系统信息"