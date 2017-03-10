# coding:utf-8
import re
import time
import urllib
import urllib2
import cookielib
class phpwind():
    def __init__(self,url,username,password,jumpurl=""):
        self.host=url
        self.username=username
        self.password=password
        self.hash=re.findall("var verifyhash = '.*?';",urllib.urlopen(self.host).read())[0][18:-2]
        self.loginurl=self.host+"/login.php?nowtime="+self.getTime()+"&verify=%s"%self.hash
        self.siginurl=self.host+'/u.php'
        self.siginsss=(self.host+"/jobcenter.php?action=punch&verify=%s&nowtime="+self.getTime()+"&verify=%s")%(self.hash,self.hash)
        self.jumpurl =jumpurl
        if self.jumpurl=='':
            self.jumpurl=self.host+"/index.php"
        self.cookie=cookielib.CookieJar()
        self.opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
    def login(self):
        postdata = urllib.urlencode({
            'ajax': '1',
            'cktime': '31536000',
            'jumpurl': self.jumpurl,
            'lgt': '0',
            'pwpwd': self.password,
            'pwuser': self.username,
            'step': '2'
        })
        self.opener.open(self.loginurl, postdata)
        result=self.opener.open(self.jumpurl)
        if len(re.findall("var windid	= '"+self.username+"';",result.read())):
            # print "login secuss"
            return True
        # print "login faild"
        return False
    def getTime(self):
        return str(time.time()).replace('.', '') + '0'
    def read(self):
        return self.opener.open(self.host).read().decode('gbk').encode('utf-8')
    def issigin(self):
        if "每日打卡" in self.opener.open(self.siginurl).read().decode('gbk').encode('utf-8'):
            return False
        return True
    def sigin(self):
        postdata = urllib.urlencode({
            'step': '2'
        })
        if "你已经打卡,请明天再试" in self.opener.open(self.siginsss, postdata).read().decode("gbk").encode("utf-8"):
            return True
        return False
    def getinfo(self):
        ret=''
        ret+='====================================='
        ret+='\n站点名称: %s'%re.findall("<title>.*?</title>",self.opener.open(self.host).read().decode("gbk").encode("utf-8"))[0][7:-8]
        ret+='\n用户: %s %s'%(self.username,"已经签到" if self.issigin() else "并没有签到" )
        for x in re.findall("<li>.{1,8}:.{1,16}</li>",self.opener.open(self.host).read().decode("gbk").encode("utf-8")):
            ret+='\n'+x[4:-5]
        ret+='\n====================================='
        return ret


# '''http://bbs.mydigit.cn/jobcenter.php?action=punch&verify=1849a44a&nowtime=1475251499535&verify=1849a44a'''

def work(msg,info):
    if not msg.content.startswith("phpwind"):
        return False
    if not info.get('level',3) < 4:
        return False
    msg=msg.content.split(' ')
    a = phpwind("http://"+msg[1], msg[2], msg[3])
    if a.login():
        return a.getinfo()
    else:
        return help(info)

def help(info):
    if not info.get('level',3) < 4:
        return False
    return "#phpwind example.com 账号 密码 phpwind登陆打卡"