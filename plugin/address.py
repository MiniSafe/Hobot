# coding:utf-8
import re
import urllib2
import json

def get_ip_information(ip):
    url = 'http://api.map.baidu.com/highacciploc/v1?qcip=' + ip + '&qterm=pc&ak='+百度地图精确定位apikey+'&coord=bd09ll&extensions=3'
    poiss = ''
    request = urllib2.Request(url)
    page = urllib2.urlopen(request, timeout=10)
    data_json = page.read()
    poiss = poiss + 'IP:' + ip + "\n"
    data_dic = json.loads(data_json)
    if (data_dic.has_key("content")):
    # if False:
        content = data_dic["content"]
        address_component = content["address_component"]
        formatted_address = content["formatted_address"]
        poiss = poiss + "该IP地址的具体位置为：\n"
        poiss = poiss + address_component["country"].encode("utf-8")
        poiss = poiss + formatted_address.encode("utf-8") + "\n"
        if (content.has_key("pois")):
            poiss = poiss + "该IP地址附近POI信息如下：\n"
            pois = content["pois"]
            for index in range(len(pois)):
                poiss = poiss + pois[index]["name"].encode("utf-8") + "\n"
                poiss = poiss + pois[index]["address"].encode("utf-8") + "\n"
    else:
        url='http://apis.baidu.com/bdyunfenxi/intelligence/ip?ip='+ip
        poiss=''
        request = urllib2.Request(url)
        request.add_header('apikey','百度商店apikey')
        page= urllib2.urlopen(request,timeout=10).read()
        page=json.loads(page)
        print page
        a = page['Base_info']['country']
        print page, type(a), repr(a),a.encode('utf-8')
        if page.get('Status',-1) != 0:
            return 'IP地址定位失败！！！'
        else:
            poiss='基本信息\n国家:%s\n'%page['Base_info']['country'].encode("utf-8")
            poiss=poiss+'省:%s\n'%page['Base_info']['province'].encode("utf-8") if page['Base_info']['province'] != None else 'None'
            poiss=poiss+'城市:%s\n'%page['Base_info']['city'].encode("utf-8") if page['Base_info']['city'] != None else 'None'
            poiss=poiss+'区县:%s\n'%page['Base_info']['county'].encode("utf-8") if page['Base_info']['county'] != None else 'None'
            poiss=poiss+'运营商:%s\n'%page['Base_info']['isp'].encode("utf-8") if page['Base_info']['isp'] != None else 'None'
            if page['Net_info']:
                poiss += '\n网络信息:\n是否提供NTP服务:%s\n'% ('提供' if page['Net_info'].get('is_ntp',None) else '不提供')
                poiss += 'NTP端口号:%s\n' % (str(page['Net_info']['ntp_port']) if page['Net_info']['ntp_port'] != -1 else "无")
                poiss += '是否提供DNS服务:%s\n' % ('提供' if page['Net_info'].get('is_dns',None) else '不提供')
                poiss += 'DNS端口号:%s\n' % (str(page['Net_info']['dns_port']) if page['Net_info']['dns_port'] != -1 else "无")
                poiss += '是否提供Proxy服务:%s\n' % ('提供' if page['Net_info'].get('is_proxy',None) else '不提供')
                poiss += 'Proxy端口号:%s\n' % (str(page['Net_info']['proxy_port']) if page['Net_info']['proxy_port'] != -1 else "无")
                poiss += '是否提供VPN服务:%s\n' % ('提供' if page['Net_info'].get('is_vpn',None) else '不提供')
                poiss += 'VPN端口号:%s' % (str(page['Net_info']['vpn_port']) if page['Net_info']['vpn_port'] != -1 else "无")
    return poiss
def work(msg,info):
    msg = msg.content.strip()
    if msg.startswith("ip") and info.get('level',3) < 4:
        try:
            msg = msg.split(' ')[-1]
            return get_ip_information(msg)
        except:
            return help(info)
    else:
        return False
def help(info):
    if info.get('level', 3) < 4:
        return '#ip 127.0.0.1  获取IP地址位置信息'
