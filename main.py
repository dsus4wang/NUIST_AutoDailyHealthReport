# -*- coding: UTF-8 -*-
import requests
import time
from bs4 import BeautifulSoup
import datetime
import json
import execjs
import pathlib
import os

def getIpdp(username, password):
     url = 'https://authserver.nuist.edu.cn/authserver/login?service=http%3A%2F%2Fauthserver.nuist.edu.cn%2Fauthserver%2Findex.do'
     # username = '201883020003'
     # password = 'Campus@dsus4'
     header = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
         'DNT': '1',
         'Host': 'authserver.nuist.edu.cn',
         'Origin': 'https://authserver.nuist.edu.cn',
         'Referer': 'https://authserver.nuist.edu.cn/authserver/login?service=http%3A%2F%2Fauthserver.nuist.edu.cn%2Fauthserver%2Findex.do'
     }
     s = requests.Session()
     r = s.get(url, timeout=5)
     htmlTextOri = r.text
     html = BeautifulSoup(htmlTextOri, 'lxml')
     pwdEncryptSalt = html.find(id='pwdEncryptSalt')['value']
     execution = html.find(id='execution')['value']
     cookies = r.cookies
     # print(cookies.values())
     with open('DailyHealthReport\encrypt.js', 'r', encoding="utf-8") as f:
         script = f.read()
     encrypt = execjs.compile(script)
     encodedPassword = encrypt.call(
         'encryptPassword', password, pwdEncryptSalt)
     # print(encodedPassword)
     data = {
         'username': '201883020003',
         'password': encodedPassword,
         'captcha': '',
         '_eventId': 'submit',
         'cllt': 'userNameLogin',
         'lt': '',
         'execution': execution,
     }
     r2 = s.post(url, data=data, cookies=cookies,
                 headers=header, timeout=5, allow_redirects=False)
     targetCookie = r2.cookies.get_dict()['iPlanetDirectoryPro']
     print(targetCookie)
     return(targetCookie)

# 运行前检查服务器正常吗
print(time.strftime('%Y-%m-%d %H:%M:%S'))
print('检查学校服务器状态...')
try:
    testSvr = requests.get('http://e-office2.nuist.edu.cn/', timeout=3).text
    testSvr = requests.get('http://authserver.nuist.edu.cn', timeout=10).text
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    print('正常，请输入用户名密码登录：')
except requests.exceptions.RequestException as e:
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    print("学校服务器崩了，请联系辅导员")
#     errorSvr = s.get('https://sc.ftqq.com/.send?text=每日打卡失败：学习服务器异常')
    exit(0)
username = input()
password = input()
print(time.strftime('%Y-%m-%d %H:%M:%S'))
s = requests.Session()
url = 'http://e-office2.nuist.edu.cn/infoplus/form/XNYQSB/start'
cookies = dict(iPlanetDirectoryPro=getIpdp(username, password))
print(cookies)
r1 = s.get(url, cookies=cookies, timeout=5)
cookieNew = r1.cookies
htmlTextOri = r1.text
html = BeautifulSoup(htmlTextOri, 'lxml')
tar1 = str(html.find_all('meta')[3])
csrfToken = tar1.split('"')[1]
url2 = 'http://e-office2.nuist.edu.cn/infoplus/interface/start'
data2 = {'idc': 'XNYQSB',
         'release': '',
         'csrfToken': csrfToken,
         'formData': '{"_VAR_URL":"http://e-office2.nuist.edu.cn/infoplus/form/XNYQSB/start","_VAR_URL_Attr":"{}"}'
         }
header2 = {'Referer': 'http://e-office2.nuist.edu.cn/infoplus/form/XNYQSB/start',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
           'Origin': 'http://e-office2.nuist.edu.cn',
           }
r2 = s.post(url2, data=data2, cookies=cookieNew,
            headers=header2, timeout=5)
targetUrl = json.loads(r2.text)['entities'][0]
stepId = int(targetUrl.split('/')[5])
t2 = int(time.time())
# 这里要自己抓包改
formData2 = ''
postData2 = {
    'actionId': 1,
    'formData': formData2,
    'remark': '',
    'rand': 185.43415117494698,
    'nextUsers': '{}',
    'stepId': stepId,
    'timestamp': t2,
    'boundFields': 'fieldCXXXjtgjbc,fieldMQJCRxh,fieldCXXXsftjhb,fieldSTQKqt,fieldSTQKglsjrq,fieldYQJLjrsfczbldqzt,fieldCXXXjtfsqtms,fieldCXXXjtfsfj,fieldJBXXjjlxrdh,fieldJBXXxm,fieldJBXXjgsjtdz,fieldCXXXsftjhbss,fieldSTQKfrtw,fieldMQJCRxm,fieldCXXXsftjhbq,fieldSTQKqtms,fieldCXXXjtfslc,fieldJBXXlxfs,fieldJBXXxb,fieldCXXXjtfspc,fieldYQJLsfjcqtbl,fieldCXXXssh,fieldJBXXgh,fieldCNS,fieldYC,fieldSTQKfl,fieldCXXXsftjwh,fieldCXXXfxxq,fieldSTQKdqstzk,fieldSTQKhxkn,fieldSTQKqtqksm,fieldFLid,fieldYQJLjrsfczbl,fieldJBXXjjlxr,fieldCXXXfxcfsj,fieldMQJCRcjdd,fieldSQSJ,fieldSTQKfrsjrq,fieldSTQKks,fieldJBXXcsny,fieldSTQKgm,fieldJBXXnj,fieldCXXXjtzzq,fieldJBXXJG,fieldCXXXdqszd,fieldCXXXjtzzs,fieldSTQKfx,fieldSTQKfs,fieldCXXXjtfsdb,fieldCXXXcxzt,fieldCXXXjtfshc,fieldCXXXjtjtzz,fieldCXXXsftjhbs,fieldJBXXsfzh,fieldSTQKsfstbs,fieldCXXXcqwdq,fieldJBXXfdygh,fieldJBXXjgshi,fieldJBXXfdyxm,fieldWXTS,fieldCXXXjtzz,fieldJBXXjgq,fieldCXXXjtfsqt,fieldJBXXjgs,fieldSTQKfrsjsf,fieldSTQKglsjsf,fieldJBXXdw,fieldCXXXsftjhbjtdz,fieldMQJCRlxfs',
    'csrfToken': csrfToken,
    'lang': 'zh',
}
url3 = 'http://e-office2.nuist.edu.cn/infoplus/interface/doAction'
header3 = {'Referer': 'http://e-office2.nuist.edu.cn/infoplus/form/'+str(stepId)+'/render',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
           'Origin': 'http://e-office2.nuist.edu.cn',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           }
r3 = s.post(url3, data=postData2, cookies=cookieNew,
            headers=header3, timeout=5)
print(time.strftime('%Y-%m-%d %H:%M:%S'))
print('成功！')
# r4 = s.get('https://sc.ftqq.com/SCKEY.send?text=每日打卡成功')
