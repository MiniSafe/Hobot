# coding:utf-8
import urllib2
import urllib


def work(msg,info):
    if not msg.content.startswith('findmima'):
        return False
    if not info.get('level',3) < 4:
        return False
    data = msg.content.split(' ')[-1]
    try:
        brow = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        brow.addheaders = []
        brow.addheaders.append(('Referer', 'http://2017.findmima.com/ajax.php?act=select'))
        brow.addheaders.append(('User-Agent',
                                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'))
        brow.addheaders.append(('Host', '2017.findmima.com'))
        brow.addheaders.append(('Content-Type', 'application/x-www-form-urlencoded'))
        brow.addheaders.append(('Accept-Language', 'zh-cn'))

        postdata = urllib.urlencode({'select_act': '3',
                                     'match_act': '1',
                                     'key': data,
                                     'table': 'myspace1'})
        ret = brow.open('http://2017.findmima.com/ajax.php?act=select', postdata).read()[3:]
        datas = ret.split(';')
        result = ''
        for x in datas:
            try:
                info = x[7:-1].split('","')
                if result:
                    result += '\n' + info[1] + ' ' + info[2]
                else:
                    result += info[1] + ' ' + info[2]
            except:
                pass
        if result:
            return result
        return '没有查到'
    except Exception, e:
        return help(info)


def help(info):
    if not info.get('level',3) < 4:
        return False
    return '#findmima data 查裤子'

