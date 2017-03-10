# coding:utf-8
def work(msg, info):
    # msg参数具体有什么方法和作用请参考 https://github.com/pandolia/qqbot
    # info 参数为从用户配置读出来的，json代码，方便以后做添加功能
    if msg.content.startswith('command'):
        if info.get('level', 3) < 2:  # 判断调用等级
            msg.Reply('sb')  # 可以直接用这个发，不会结束函数调用
            return 'sb'  # 处理命令并且返回
    else:
        return False


def help(info):  # 执行help命令会执行所有插件的help命令，返回不是一个字符串就做没有返回参数处理
    if info.get('level', 3) < 2:  # 判断调用等级
        return '这个是sb的帮助信息'
