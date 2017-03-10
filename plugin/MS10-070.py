# coding:utf-8
import base64
import urllib2
import threading

def check(ip, port, timeout,msg):
    try:
        url = 'http://' + ip + ":" + str(port)
        res_html = urllib2.urlopen(url, timeout=timeout).read()
        if 'WebResource.axd?d=' in res_html:
            error_i = 0
            bglen = 0
            for k in range(0, 255):
                IV = "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" + chr(k)
                bgstr = 'A' * 21 + '1'
                enstr = base64.b64encode(IV).replace('=', '').replace('/', '-').replace('+', '-')
                exp_url = "%s/WebResource.axd?d=%s" % (url, enstr + bgstr)
                try:
                    request = urllib2.Request(exp_url)
                    res = urllib2.urlopen(request, timeout=timeout)
                    res_html = res.read()
                    res_code = res.code
                except urllib2.HTTPError, e:
                    res_html = e.read()
                    res_code = e.code
                except urllib2.URLError, e:
                    error_i += 1
                    if error_i >= 3: return
                except:
                    return
                if int(res_code) == 200 or int(res_code) == 500:
                    if k == 0:
                        bgcode = int(res_code)
                        bglen = len(res_html)
                    else:
                        necode = int(res_code)
                        if (bgcode != necode) or (bglen != len(res_html)):
                            msg.Reply(ip+' MS10-070 ASP.NET Padding Oracle信息泄露漏洞')
                else:
                    return
    except Exception, e:
        msg.Reply('扫描出错')


def work(msg,info):
    msg.content = msg.content.strip()
    if msg.content.startswith("ms10-070"):
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
    return '#ms10-070 ip [port] MS10-070 .NET Padding Oracle信息泄露"'
