# coding:utf-8
def work(msg,info):
    msg=msg.content.strip()
    if msg.startswith("我的权限"):
        level=info.get('level', 3)
        if level>3:
            return '恭喜您，您现在在黑名单'
        elif level==3:
            return '您的权限是:狗群员'
        elif level==2:
            return '您的权限是:高级狗群员'
        elif level==1:
            return '您的权限是:狗管理'
        else:
            return '您的权限是:超级狗管理'
    else:
        return False
def help(info):
    return "#我的权限 查看自己的权限"