# coding:utf-8
import urllib2
import urllib
import json
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

city = {}


def load():
    global city
    for server in re.findall('\{t: ".*?",v: "\d*?",status:"1", display:"1", opt_data_array:\[\]\}', urllib2.urlopen(
            'http://gameact.qq.com/comm-htdocs/js/game_area/bns_server_select.js').read().decode('gbk').encode('utf-8')[
                                                                                                    263:-2949]):
        _, name, _, id, _ = server.split('"', 4)
        if name.count('（') > 0:
            name = name.split('（')[0]
        elif name.count('(') > 0:
            name = name.split('(')[0]
        city[name] = id


load()
def getBagua(info):
    result=[]
    result.append('1 ' + info[1] + '   2 ' + info[2])
    result.append('3 ' + info[3] + '   4 ' + info[4])
    result.append('5 ' + info[5] + '   6 ' + info[6])
    result.append('7 ' + info[7] + '   8 ' + info[8])
    return result

def getInfo(add, name):
    if city.has_key(add):
        brow = urllib2.build_opener()
        brow.addheaders = [('User-agent',
                            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'),
                           ('Referer',
                            'http://bang.qq.com/tool/bns/jsqb.htm?serverId=' + city.get(add) + '&roleName=' + name)]
        print 'http://bang.qq.com/tool/bns/jsqb.htm?serverId=' + city.get(add) + '&roleName=' + name
        userinfo = json.loads(brow.open('http://bang.qq.com/ugc1/getJsqbData',
                                        urllib.urlencode({'serverId': city.get(add), 'roleName': name})).read())
        result = []
        result.append('昵称 : ' + name + '  等级 : ' + str(userinfo['data']['level']) + ' 级  星级 : ' + str(
            userinfo['data']['mlevel']) + " 星")
        result.append('种族 : ' + {1: "天", 2: "龙", 3: "灵", 4: "人"}[int(userinfo['data']['race'])] + '  职业 : ' +
                      {1: "剑士", 2: "拳师", 3: "气功师", 5: "力士", 6: "召唤师", 7: "刺客", 8: "灵剑士", 9: "咒术师", 10: '气宗师'}[
                          int(userinfo['data']['job'])])
        zhuangbei = userinfo['data']['item']
        tmp = ''
        for zb in zhuangbei:
            if zb['type'] == 'gem':
                continue
            if tmp == "" or tmp[-1] == '\n':
                tmp += zb['name'] + '     '
            else:
                tmp += zb['name'] + '\n'
        result.append(tmp[:-1])
        tmp = {}
        for zb in zhuangbei:
            if zb['type'] != 'gem':
                continue
            tmp[zb['pos']] = zb['name']
        result.extend(getBagua(tmp))
        return '\n'.join(result)
    else:
        return '您输入的参数有误'


def work(msg, info):
    msg = msg.content.strip()
    if msg.startswith("剑灵"):
        level = info.get('level', 3)
        if level < 4:
            try:
                _, add, name = msg.split(' ')
                return getInfo(add, name)
            except Exception, e:
                print e
                return help(info)
    else:
        return False


def help(info):
    if info.get('level', 3)<4:
        return "#剑灵 独战群雄 络"
