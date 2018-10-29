#-*- coding:utf-8 -*-

import requests,random,json,re,os,xlwt,xlrd,time
from hashlib import  md5
from bs4 import BeautifulSoup
from multiprocessing import Pool
from configobj import ConfigObj
from xlrd import open_workbook
from xlutils.copy import copy
from urllib.parse import urlencode
from requests.exceptions import RequestException
from emailSend import Email
from excelInfo import infoExcel
from ipProxy import ip_infoIni

# 读取config.ini文件
cf = ConfigObj("config.ini",encoding='UTF8')
# 日期格式化
date = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))

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

# 随机选择header
def get_random_header():
    headers={
        'Host': getHeadValue('host'),
        'User-Agent':random.choice(list),
        'Referer': getHeadValue('referer')
    }
    return headers

def get_page_index(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 1,
        'from':'search_tab'
    }
    # 读取代理ip信息
    ipProxys=isProxy()

    if ipProxys:
        proxies = {
            ipProxys[0][0]: ipProxys[0][0]+'://'+ipProxys[0][1]+':'+ipProxys[0][2]
        }
    # 字典类型转url请求参数
    # 这是ajax请求的网址,不要忘了问号
    url = getConfValue('url') + urlencode(data)
    try:
        # 使用代理
        if (getProxyValue('isproxy')=='True'):
            print('使用代理ip: ',ipProxys)
            response = requests.get(url, headers=get_random_header(), proxies=proxies)
        # 不使用代理
        else :
            response = requests.get(url, headers=get_random_header())
        if response.status_code == 200:
            return response.json()
        return None
    except RequestException:
        print("请求索引出错")
        return None

def parse_page_index(html):
    page_json=[]
    page_datas = []
    datas = json.loads(html)
    #如果data在键名中
    if datas['data']:
        #迭代data字典中的数据
        dataList = datas['data']
        for item in dataList:
            if 'open_url' in item.keys():
                title = item['title']
                article_url = item['article_url']
                comment_count = item['comment_count']
                datetime = item['datetime']
                has_video = item['has_video']
                if date in datetime :
                    page_json.append([str(datetime),str(title),str(comment_count),str(has_video),str(article_url)])
        page_datas.append([page_json])
    return page_datas

# 数据请求获取网页数据
def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print("请求详情页出错", url)
        return None

def save(page_data,filename):
    # print(page_data)
    for data in page_data:
        if data :
            infoExcel(data,filename)

def emailSend(filename):
    sender=getEmailValue('sender')
    mypass=getEmailValue('mypass')
    receiver=getEmailValue('receiver')
    keyword=getConfValue('keyword')
    res = Email(filename,sender,mypass,receiver,keyword)
    if res:
        print('邮件发送成功')
    else:
        print('邮件发送失败')

#获取配置文件name对应值
def getConfValue(name):
    return cf['conf'][name]
def getHeadValue(name):
    return cf['head'][name]
def getProxyValue(name):
    return cf['proxy'][name]
def getEmailValue(name):
    return cf['email'][name]

def getDictDatas_FromFile(fs):
    lines = fs.readlines()  # 按行读取
    data = []   # 定义一个空列表，用来接收每行数据
    for line in lines:
        list = line.strip("\n").split(",")  # 用，号分隔，并去除换行符
        urls = {}   # 定义一个空字典
        for item in list:   # 获取list列表中的每一条数据
            temp = item.split(":",1)    # 将list中每一条数据用 ：号分隔1次
            urls[temp[0]] = temp[1] # 键-值对添加值  key = value
        data.append(urls)
    return data

def get_ips():
    result=[]
    flag = 'False'
    checkIpProxy = ['http', 'https']
    httpTxt = 'ip_http.txt'
    httpsTxt = 'ip_https.txt'
    try:
        # 随机获取http或者https
        checkIp = random.choice(checkIpProxy)
        # print(checkIp)
        if checkIp == 'http':
            try:
                fs = open(httpTxt, encoding='utf-8')  # 打开文件
                ips = getDictDatas_FromFile(fs)
                result.append([checkIp,ips])
                return result
            except:
                try:
                    fs = open(httpsTxt, encoding='utf-8')  # 打开文件
                    ips = getDictDatas_FromFile(fs)
                    result.append([checkIp, ips])
                    return result
                except:
                    return None
        else:
            try:
                fs = open(httpsTxt, encoding='utf-8')  # 打开文件
                ips = getDictDatas_FromFile(fs)
                result.append([checkIp,ips])
                return result
            except:
                try:
                    fs = open(httpTxt, encoding='utf-8')  # 打开文件
                    ips = getDictDatas_FromFile(fs)
                    result.append([checkIp, ips])
                    return result
                except:
                    return None
        return None
    except:
        return None

def isProxy():
    ipProxys=[]
    try:
        if (getProxyValue('isproxy')=='True'):
            # 获取代理ip信息
            result = get_ips()
            if result:
                httpType = result[0][0]
                ips = result[0][1]
                # print(httpType)
                try:
                    ip = random.choice(ips)
                except:
                    print('没有可用代理ip')
                    return ipProxys
                for key in ip:
                    # print(key)
                    # print(ip[key])
                    ipProxys.append([httpType,key,ip[key]])
                    # print("代理ip: ",ipProxys)
                    return ipProxys
        return ipProxys
    except:
        return ipProxys


def main(offset):
    time.sleep(3)
    #获得的是json形式返回的数据
    html = get_page_index(offset,getConfValue('keyword'))
    filename = getConfValue('titel') + date + '.xls'
    if html:
        data = json.dumps(html)
        page_datas = parse_page_index(data)
        for page_data in page_datas:
            if page_data:
                try:
                    save(page_data,filename)
                except:
                    continue

if __name__ == '__main__':

    # 程序开始时间
    time_start = time.time()

    filename = getConfValue('titel') + date + '.xls'
    time.sleep(5)
    start = 1
    end = 20
    #构造一个list，设置offset参数，实现下滑加载请求
    groups = [x*20 for x in range(start, end+1)]
    pool = Pool()
    #需要执行的函数，可迭代对象
    pool.map(main, groups)
    # # 发送邮件
    emailSend(filename)

    # 程序结束时间
    time_end = time.time()
    print('耗时: '+str(time_end - time_start)+'秒')
    time.sleep(5)
    print('程序执行完成')