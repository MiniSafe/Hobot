# coding:utf-8
import urllib2
import re

def work(msg,info):
    if not msg.content.startswith('check'):
        return False
    if not info.get('level',3) < 4:
        return False
    addr = msg.content.split(' ')[-1]
    addr = addr.strip('/').strip('http://').strip('https://')
    try:
        request = urllib2.Request('http://dns.aizhan.com/' + addr + '/', headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'})
        page = urllib2.urlopen(request, timeout=50).read()
        # print page
        result = ""
        print page
        for text in re.findall(
                '<table width="100%" class="table" id="getmeas" style="border-top:none">[\w\W]*?</table>', page):
            text = text.split('<tr>')[2:]
            print text
            for lines in text:
                print lines
                line = re.findall('<a[\w\W]*?</a>', lines)
                domain = line[0].split('"')[1]
                name = '获取失败'
                if len(line) > 1:
                    name = line[1].split('>')[1].split('<')[0]
                result += '\n' + domain + '   ' + name
        if result:
            temp = re.findall('当前域名[\w\W]*?个域名解析到该IP。', page)[0]
            address = temp.split(">")[3].split('<')[0]
            city = temp.split('>')[5].split('<')[0]
            num = temp.split('>')[7].split('<')[0]
            return '您查询的:' + addr + '\nIP地址:' + address + '\n所在地区:' + city + '，共有' + num + "个域名解析到该IP" + result
        else:
            return '没有查询到信息'
    except Exception, e:
        print e
        return help(info)


def help(info):
    if not info.get('level',3) < 4:
        return False
    return '#check example.com 查询同IP站点'
