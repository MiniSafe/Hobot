# coding:utf-8
def work(msg,info):
    msg=msg.content.strip()
    if msg.startswith("parsetv"):
        if not info.get('level', 3) < 4:
            return False
        try:
            msg=msg.split(' ',1)[1]
            return 'http://api.nepian.com/ckparse/web.php?url='+msg
        except:
            return help(info)
    else:
        return False
def help(info):
    if not info.get('level',3) < 4:
        return False
    return "#parsetv e.com 解析爱奇艺、优酷、土豆、乐视、芒果TV等"