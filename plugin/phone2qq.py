#! /usr/bin/env python3
# -*- coding: utf-8 -*-

''' https://github.com/zrools/phone2qq '''

import socket
import hashlib
from random import randint
from binascii import a2b_hex, b2a_hex, unhexlify


def bytearrays(param):
    # s = unhexlify(param)
    # b = [ord(x) for x in s]
    # return b
    return str(bytearray.fromhex(param))


import struct, ctypes
from random import randint

__all__ = ['encrypt', 'decrypt']


def xor(a, b):
    a1, a2 = struct.unpack('!LL', a[0:8])
    b1, b2 = struct.unpack('!LL', b[0:8])
    r = struct.pack('!LL', a1 ^ b1, a2 ^ b2)
    return r


def encipher(v, k):
    n = 16
    delta = 0x9e3779b9
    k = struct.unpack('!LLLL', k[0:16])
    y, z = map(ctypes.c_uint32, struct.unpack('!LL', v[0:8]))
    s = ctypes.c_uint32(0)
    for i in range(n):
        s.value += delta
        y.value += (z.value << 4) + k[0] ^ z.value + s.value ^ (z.value >> 5) + k[1]
        z.value += (y.value << 4) + k[2] ^ y.value + s.value ^ (y.value >> 5) + k[3]
    r = struct.pack('!LL', y.value, z.value)
    return r


def encrypt(v, k):
    vl = len(v)
    filln = (6 - vl) % 8
    v_arr = [
        bytes(bytearray([filln | 0xf8])),
        b'\xad' * (filln + 2),
        v,
        b'\0' * 7,
    ]
    v = b''.join(v_arr)
    tr = b'\0' * 8
    to = b'\0' * 8
    r = []
    o = b'\0' * 8
    for i in range(0, len(v), 8):
        o = xor(v[i:i + 8], tr)
        tr = xor(encipher(o, k), to)
        to = o
        r.append(tr)
    r = b''.join(r)
    return r


def decrypt(v, k):
    l = len(v)
    prePlain = decipher(v, k)
    # print prePlain
    pos = ord(bytes(prePlain[0])) & 0x07 + 2
    r = prePlain
    preCrypt = v[0:8]
    for i in range(8, l, 8):
        x = xor(decipher(xor(v[i:i + 8], prePlain), k), preCrypt)
        prePlain = xor(x, preCrypt)
        preCrypt = v[i:i + 8]
        r += x
    if r[-7:] == b'\0' * 7:
        return r[pos + 1:-7]


def decipher(v, k):
    n = 16
    y, z = map(ctypes.c_uint32, struct.unpack('!LL', v[0:8]))
    a, b, c, d = map(ctypes.c_uint32, struct.unpack('!LLLL', k[0:16]))
    delta = 0x9E3779B9
    s = ctypes.c_uint32(delta << 4)
    for i in range(n):
        z.value -= ((y.value << 4) + c.value) ^ (y.value + s.value) ^ ((y.value >> 5) + d.value)
        y.value -= ((z.value << 4) + a.value) ^ (z.value + s.value) ^ ((z.value >> 5) + b.value)
        s.value -= delta
    return struct.pack('!LL', y.value, z.value)


def md5(cstr):
    m = hashlib.md5()
    m.update(cstr.encode())
    return m.hexdigest().lower()


class QQLogin():
    def __init__(self):
        self.num = '10000000000'  # 手机号
        self.address = ('183.60.56.100', 8000)  # 企鹅服务器
        self.fixedData = '0000044b0000000100001509'  # 填充数据
        self.hdKey = '0251ca4aab66e80ae4d279921ace3c3dfee23788151f45368d'
        self.serverIP = ''
        self.serverTime = ''
        self.token0825 = ''

    def str2hex(self, mStr):
        text = ''
        for x in mStr:
            text += '3%s' % x
        return text

    def getSequence(self, length):
        text = ''
        for l in range(length):
            text += '%02x' % randint(0, 0xff)
        return text

    def login0825(self):
        key0825 = '7792394f1afd3bbfa9006bc807bcf23b'

        data = '0235550825'  # head
        data += self.getSequence(2)
        data += '00000000'  # QQ Hex
        data += '030000000101010000674200000000'
        data += key0825

        txt = '001800160001'
        txt += self.fixedData
        txt += '0000000000000000'
        txt += '0004000f0000000b'
        txt += self.str2hex(self.num)
        txt += '0309'
        txt += '0008'
        txt += '0001000000000004'
        txt += '00360012'
        txt += '000200010000000000000000000000000000'
        txt += '0114001d01020019'
        txt += self.hdKey

        data += b2a_hex(encrypt(bytearrays(txt), bytearrays(key0825))).decode()
        data += '03'
        data = a2b_hex(data)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data, self.address)
        recvPack = sock.recv(1024)
        sock.close()

        recvData = b2a_hex(decrypt(recvPack[14:-1], bytearrays(key0825))).decode()

        if (recvData[:2] != '00'):
            recvData = recvData[16:]

        if (recvData[:2] == '00'):
            self.token0825 = recvData[10:122]
            self.serverTime = recvData[134:142]
            self.serverIP = recvData[166:174]
            return self.login0826()
        else:
            print('0825 error!')
            return False

    def login0826(self):
        key0826 = '6d47535a5a573d4872772c2d36717a76'
        keyCode = '13d924ca5e0469d284effea87a5a5f1c'

        data = '02355508366848'  # head
        data += '00000000'
        data += '0300000001010100006742'
        data += '00000000'
        data += '000101020019'
        data += self.hdKey
        data += '00000010'
        data += self.getSequence(16)

        txt = '01120038'
        txt += self.token0825
        txt += '030f0008000657494e444f57'  # WINDOWS
        txt += '0004000f0000000b'
        txt += self.str2hex(self.num)
        txt += '00060078'

        md5p = md5('123456')
        # 密码加密
        pwd = md5p
        pwd += '00000000'
        pwd += '00000000'  # QQ Hex

        # 密匙加密
        key = 'F36251810002'
        key += '00000000'  # QQ Hex
        key += self.fixedData
        key += '000001'
        key += md5p
        key += self.serverTime
        key += '00000000000000000000000000'
        key += self.serverIP
        key += '000000000000000600101ba49e165fe954251eb9619f7b1bdf31'
        key += key0826

        txt += b2a_hex(encrypt(bytearrays(key), bytearrays(pwd))).decode()

        # region CRC
        txt += '001500300000'
        txt += '01'
        txt += '1c26e960'
        txt += '0010'
        txt += '028d5f75cbcf4c898ca43a3410b85788'
        txt += '02'
        txt += 'b3e8163c'
        txt += '0010'
        txt += '1ba49e165fe954251eb9619f7b1bdf31'
        txt += '001a'
        txt += '0040'

        mcrc = '001500300000'
        mcrc += '01'
        mcrc += '1c26e960'
        mcrc += '0010'
        mcrc += '028d5f75cbcf4c898ca43a3410b85788'
        mcrc += '02'
        mcrc += 'b3e8163c'
        mcrc += '0010'
        mcrc += '1ba49e165fe954251eb9619f7b1bdf31'

        txt += b2a_hex(encrypt(bytearrays(mcrc), bytearrays(key0826))).decode()

        txt += '001800160001'
        txt += self.fixedData
        txt += '00000000'  # QQ Hex
        txt += '00010000010300140001'
        txt += '0010'
        txt += 'bd41fd502a59f4863ccde044bb41f728'
        txt += '0312000501000000'
        txt += '00'  # 是否记住密码
        txt += '010200620001'
        txt += '1169a81f699f52de71ef65e9b42d2d8a'
        txt += '0038'
        txt += '78b94e76767efdab4dd3b2b0144063f48b57ee27aef152a28aba1f03'
        txt += '50f02b17a86787fe47d1b189c43c0be7a7dc8c81c40bb622c78ec85b'
        txt += '0014'
        txt += '62e172e61421fe8c850c62891efcf7f93a19b892'

        data += b2a_hex(encrypt(bytearrays(txt), bytearrays(keyCode))).decode()
        data += '03'
        data = a2b_hex(data)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data, self.address)
        recvPack = sock.recv(1024)
        sock.close()

        recvData = b2a_hex(decrypt(recvPack[14:-1], bytearrays(keyCode))).decode()

        if recvData[:2] == '06':
            qq = str(int(recvData[6:14], 16))
        else:
            recvData = recvData[8:]
            if recvData[:2].lower() == 'fc':
                qq = str(int(recvData[14:22], 16))
            else:
                qq = False

        return qq

    def getQQ(self, phone):
        self.num = phone
        return self.login0825()


def work(msg,info):
    msg = msg.content.strip()
    if msg.upper().startswith("QQ"):
        if not info.get('level', 3) < 4:
            return False
        try:
            msg = msg.split(' ')[-1]
            if len(msg) != 11 or not msg.isdigit():
                return '手机号有误'
            print msg
            login = QQLogin()
            qq = login.getQQ(msg)
            if qq:
                return '手机号:' + msg + '\n解析的QQ为:' + qq
            else:
                return '手机号:' + msg + '\n解析QQ失败'
        except:
            return help(info)
    else:
        return False


def help(info):
    if not info.get('level',3) < 4:
        return False
    return "#QQ 手机号 获取可以通过手机号登陆的QQ"
