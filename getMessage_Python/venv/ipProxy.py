#-*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from configobj import ConfigObj
import time,threading,random,telnetlib,requests,socket,os

#设置全局超时时间为3s，也就是说，如果一个请求3s内还没有响应，就结束访问，并返回timeout（超时）
socket.setdefaulttimeout(3)
# 读取config.ini文件
cf = ConfigObj("config.ini",encoding='UTF8')

list= [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
httpTxt = 'ip_http.txt'
httpsTxt = 'ip_https.txt'

def getProxyValue(name):
    return cf['proxy'][name]

def get_ip():
    headers = {
        'User-Agent': random.choice(list)
    }
    #获取代理IP，返回列表
    httpResult=[]
    httpsResult=[]
    proxies={
        getProxyValue('httptype'):getProxyValue('httptype')+'://'+getProxyValue('ip')
    }
    try:
        for page in range(1,2):
            IPurl = 'http://www.xicidaili.com/nn/%s' %page
            # 使用代理
            if (getProxyValue('getipproxy') == 'True'):
                print('使用代理ip: ', ipProxys)
                rIP = requests.get(IPurl, headers=headers, proxies=proxies)
            # 不使用代理
            else:
                rIP = requests.get(IPurl, headers=headers)
            IPContent=rIP.text
            # print (IPContent)
            soupIP = BeautifulSoup(IPContent,'html.parser')
            trs = soupIP.find_all('tr')
            for tr in trs[1:]:
                tds = tr.find_all('td')
                ip = tds[1].text.strip()
                port = tds[2].text.strip()
                protocol = tds[5].text.strip()
                if protocol == 'HTTP':
                    httpResult.append( 'http://' + ip + ':' + port)
                elif protocol =='HTTPS':
                    httpsResult.append( 'https://' + ip + ':' + port)
    except:
        pass
    return httpResult,httpsResult
'''
#验证ip地址的可用性，使用telnetlib模块_http
def cip(x,y):
    f = open("E:\ip_http.txt","a")
    f.truncate()
    try:
        telnetlib.Telnet(x, port=y, timeout=5)
    except:
        print('f')
    else:
        print('---------------------------success')
        f.write(x+':'+y+'\n')
#验证ip地址的可用性，使用telnetlib模块_https
def csip(x,y):
    f = open("E:\ip_https.txt","a")
    f.truncate()
    try:
        telnetlib.Telnet(x, port=y, timeout=5)
    except:
        print('f')
    else:
        print('---------------------------success')
        f.write(x+':'+y+'\n')
'''
#验证ip地址的可用性，使用requests模块，验证地址用相应要爬取的网页 http
def cip(x,y):
    f = open(httpTxt,"a")
    f.truncate()
    try:
        # print (x+y)
        requests.get('http://ip.chinaz.com/getip.aspx',proxies={'http':x+':'+y},timeout=3)
    except Exception as e:
        pass
    else:
        # print('---------------------------success')
        f.write(x+':'+y+'\n')
#验证ip地址的可用性，使用requests模块，验证地址用相应要爬取的网页。https
def csip(x,y):
    f = open(httpsTxt,'a')
    f.truncate()
    try:
        # print (x+y)
        requests.get('https://www.lagou.com/',proxies={'https':x+":"+y},timeout=3)
    except Exception as e:
        pass
    else:
        f.write(x+':'+y+'\n')

def ip_infoIni():
    httpResult,httpsResult = get_ip()
    threads = []
    open(httpTxt,"a").truncate()
    for i in httpResult:
        a = str(i.split(":")[-2][2:].strip())
        b = str(i.split(":")[-1].strip())
        t = threading.Thread(target=cip,args=(a,b,))
        threads.append(t)

    for i in range(len(httpResult)):
        threads[i].start()
    for i in range(len(httpResult)):
        threads[i].join()

    threads1 = []
    open(httpsTxt,"a").truncate()
    for i in httpsResult:
        a = str(i.split(":")[-2][2:].strip())
        b = str(i.split(":")[-1].strip())
        t = threading.Thread(target=csip,args=(a,b,))
        threads1.append(t)

    for i in range(len(httpsResult)):
        threads1[i].start()
    for i in range(len(httpsResult)):
        threads1[i].join()

def proxyIsExsit(txtName):
    try:
        fs = open(httpTxt, encoding='utf-8')  # 打开文件
        lines = fs.readlines()  # 按行读取for line in lines:
        lineNum = len(lines[0].strip())
        return lineNum
    except Exception as e:
        return 0

def checkTxt():
    line1 = proxyIsExsit(httpTxt)
    line2 = proxyIsExsit(httpsTxt)
    print(line1,line2)
    if line1 == 0 and line2 == 0:
        ip_infoIni()
    else:
        return 'True'

def main():
    try:
        if open(httpTxt):
            os.remove(httpTxt)
    except:
        pass
    try:
        if open(httpsTxt):
            os.remove(httpsTxt)
    except:
        pass
    # 爬取代理ip
    ip_infoIni()
    tag='False'
    for i in range(0, 3):
        if checkTxt()=='True':
            print('代理ip地址获取成功...')
            tag='True'
            return
    if tag == 'False':
        print('代理ip地址获取失败...')
if __name__ == '__main__':
    main()

