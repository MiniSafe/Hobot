# coding:utf-8
import pythonwhois
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def work(msg,info):
    msg = msg.content.strip()
    if msg.startswith("whois"):
        if not info.get('level', 3) < 4:
            return False
        try:
            msg = msg.split(' ')[-1]
            msg = msg.strip('/')
            if msg.count('://'):
                msg = msg.split("://")[1]
            result = pythonwhois.get_whois(msg)
            update = result.get('updated_date', None)
            create = result.get('creation_date', None)
            contacts = result.get('contacts', None)
            raw = result.get('raw', None)
            ret = ""
            if create:
                ret += '\n创建时间:' + str(create[0])
            if update:
                ret += '\n更新时间:' + str(update[0])
            if contacts:
                info = contacts.get('registrant',{})
                if not info:
                    info = contacts.get('admin', {})
                if not info:
                    info={}
                if info.get('city', None):
                    ret += '\n城市:' + str(info.get('city', None))
                if info.get('fax', None):
                    ret += '\n传真:' + str(info.get('fax', None))
                if info.get('name', None):
                    ret += '\n名字:' + str(info.get('name', None))
                if info.get('state', None):
                    ret += '\n地区:' + str(info.get('state', None))
                if info.get('phone', None):
                    ret += '\n电话:' + str(info.get('phone', None))
                if info.get('street', None):
                    ret += '\n街道:' + str(info.get('street', None))
                if info.get('country', None):
                    ret += '\n国家:' + str(info.get('country', None))
                if info.get('postalcode', None):
                    ret += '\n邮编:' + str(info.get('postalcode', None))
                if info.get('organization', None):
                    ret += '\n组织:' + str(info.get('organization', None))
                if info.get('email', None):
                    ret += '\n邮箱:' + str(info.get('email', None))
            if not ret and raw:
                return str(raw[0])
            return '域名:' + msg + ret
        except Exception, e:
            print e

            return help(info)
    else:
        return False


def help(info):
    if not info.get('level',3) < 4:
        return False
    return "#whois example.com 字面意思"
