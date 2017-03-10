#coding:utf-8
import json
import os
def work(msg,info):
    if not msg.content.startswith('token'):
        return False
    if not info.get('level',3) < 1:
        return False
    try:
        _,command,qq=msg.content.split(' ',2)
        if command=='get':
            text=''
            if os.path.exists('users/'+qq+'.ini'):
                text=open('users/'+qq+'.ini').read()

            text=text.strip('\n').strip('\r').strip(' ')
            if text=='':
                return 'QQ:'+qq+' 等级为:狗群员'
            else:
                tmp=json.loads(text).get('level', 3)
                if tmp>3:
                    return 'QQ:' + qq + ' 等级为:黑名单'
                elif tmp==3:
                    return 'QQ:' + qq + ' 等级为:狗群员'
                elif tmp==2:
                    return 'QQ:' + qq + ' 等级为:高级狗群员'
                elif tmp==1:
                    return 'QQ:' + qq + ' 等级为:狗管理'
                else:
                    return 'QQ:' + qq + ' 等级为:超级狗管理'
        else:
            qq,level=qq.split(' ')
            text=''
            if os.path.exists('users/' + qq + '.ini'):
                text = open('users/' + qq + '.ini').read()
            text = text.strip('\n').strip('\r').strip(' ')
            if text=='':
                tlevel=3
                try:
                    tlevel=int(level)
                except:
                    try:
                        tlevel={'黑名单':4,'狗群员':3,'高级狗群员':2,'狗管理':1,'超级狗管理':0}.get(level,3)
                    except:
                        return '小伙子搞事是吧'

                tmp={}
                tmp['level']=tlevel
                tmp=json.dumps(tmp)
                f=open('users/' + qq + '.ini','w')
                f.write(tmp)
                f.close()
                return '用户权限修改成功'
            else:
                tmp = json.loads(text)
                tlevel = 3
                try:
                    tlevel = int(level)
                except:
                    try:
                        tlevel = {'黑名单': 4, '狗群员': 3, '高级狗群员': 2, '狗管理': 1, '超级狗管理': 0}.get(level, 3)
                    except:
                        return '小伙子搞事是吧'
                tmp['level'] = tlevel
                f = open('users/' + qq + '.ini','w')
                f.write(json.dumps(tmp))
                f.close()
                return '用户权限修改成功'
    except Exception,e:
        print e
        return help(info)
def help(info):
    if not info.get('level',3) < 1:
        return False
    return "#token get|set QQ level(0-4) 设置权限"

# class Msg:
#     content='token 设置狗群员的等级 2358913531 狗管理'
#
# print work(Msg,{'level':0})

