#coding:utf-8
import urllib2
import re
def work(msg,info):
    if not msg.content.startswith('phone'):
        return False
    if not info.get('level',3) < 4:
        return False
    phone=msg.content.split(' ')[-1]
    if len(phone)!=11:
        return '手机号有误'
    try:
        request = urllib2.Request('http://www.ip138.com:8080/search.asp?mobile='+phone+'&action=mobile',headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                        'Referer': 'http://www.ip138.com:8080/search.asp?mobile='+phone+'^&action=mobile'})
        page=urllib2.urlopen(request,timeout=2).read().decode('gb2312').encode('utf-8')
        result=""
        for text in re.findall('<TD width=\"138\" align=\"center\".*?</TD>[\w\W]*?</TD>',page)[1:]:
            text=text.replace('\n','').replace(' ','')
            result+='\n'+text.split('>')[1].split('<')[0].replace('&nbsp;','')+':'+text.split('>')[-2].split('<')[0].replace('&nbsp;','')
        if result:
            return '您查询的:'+phone+result
        else:
            return '没有查询到信息'
    except:
        return help(info)

def help(info):
    if not info.get('level',3) < 4:
        return False
    return '#phone 13800138000 查询归属地'
