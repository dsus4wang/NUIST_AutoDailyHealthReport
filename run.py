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
    errorSvr = s.get('https://sc.ftqq.com/SCU156261Taa91200284745d9a18bad93b3f08260a6013e84603625.send?text=每日打卡失败：学习服务器异常')
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
formData2 = '''{"_VAR_EXECUTE_INDEP_ORGANIZE_Name":"计算机与软件学院-姚小芹","_VAR_ACTION_INDEP_ORGANIZES_Codes":"20900\\n20900-880084","_VAR_ACTION_REALNAME":"王封茗","_VAR_ACTION_ORGANIZE":"20900-880084","_VAR_EXECUTE_ORGANIZE":"20900-880084","_VAR_ACTION_INDEP_ORGANIZE":"20900","_VAR_ACTION_INDEP_ORGANIZE_Name":"计算机与软件学院","_VAR_ACTION_ORGANIZE_Name":"计算机与软件学院-姚小芹","_VAR_EXECUTE_ORGANIZES_Names":"计算机与软件学院-姚小芹","_VAR_OWNER_ORGANIZES_Codes":"20900\\n20900-880084","_VAR_ADDR":"123.170.92.30","_VAR_OWNER_ORGANIZES_Names":"计算机与软件学院\\n计算机与软件学院-姚小芹","_VAR_URL":"http://e-office2.nuist.edu.cn/infoplus/form/'''+str(stepId)+'''/render","_VAR_EXECUTE_ORGANIZE_Name":"计算机与软件学院-姚小芹","_VAR_RELEASE":"true","_VAR_NOW_MONTH":"2","_VAR_ACTION_USERCODES":"201883020003","_VAR_ACTION_EMAIL":"201883020003@nuist.edu.cn","_VAR_ACTION_ACCOUNT":"201883020003","_VAR_ACTION_INDEP_ORGANIZES_Names":"计算机与软件学院\\n计算机与软件学院-姚小芹","_VAR_OWNER_ACCOUNT":"201883020003","_VAR_ACTION_ORGANIZES_Names":"计算机与软件学院\\n计算机与软件学院-姚小芹","_VAR_STEP_CODE":"Tbxx","_VAR_OWNER_USERCODES":"201883020003","_VAR_EXECUTE_ORGANIZES_Codes":"20900-880084","_VAR_NOW_DAY":"'''+str(datetime.datetime.now().day)+'''","_VAR_OWNER_EMAIL":"201883020003@nuist.edu.cn","_VAR_OWNER_REALNAME":"王封茗","_VAR_NOW":"'''+str(t2)+'''","_VAR_URL_Attr":"{}","_VAR_ENTRY_NUMBER":"3694279","_VAR_EXECUTE_INDEP_ORGANIZES_Names":"计算机与软件学院-姚小芹","_VAR_STEP_NUMBER":"'''+str(stepId)+'''","_VAR_POSITIONS":"20900:2\\n20900-880084:002:201883020003","_VAR_EXECUTE_INDEP_ORGANIZES_Codes":"20900-880084","_VAR_EXECUTE_POSITIONS":"20900-880084:002:201883020003","_VAR_ACTION_ORGANIZES_Codes":"20900\\n20900-880084","_VAR_EXECUTE_INDEP_ORGANIZE":"20900-880084","_VAR_NOW_YEAR":"2021","groupMQJCRList":[0],"fieldFLid":"","fieldSQSJ":'''+str(
    t2)+''',"fieldJBXXxm":"201883020003","fieldJBXXxm_Name":"王封茗","fieldJBXXgh":"201883020003","fieldJBXXxb":"1","fieldJBXXxb_Name":"男（male）","fieldJBXXlxfs":"18502556668","fieldJBXXdw":"20900-880084","fieldJBXXdw_Name":"计算机与软件学院-姚小芹","fieldJBXXnj":"18软合1班","fieldJBXXsfzh":"371121199911330417","fieldJBXXJG":"1","fieldJBXXcsny":"","fieldJBXXfdyxm":"","fieldJBXXfdyxm_Name":"","fieldJBXXfdygh":"","fieldJBXXjgs":"370000","fieldJBXXjgs_Name":"山东省","fieldJBXXjgshi":"371100","fieldJBXXjgshi_Name":"日照市","fieldJBXXjgshi_Attr":"{\\"_parent\\":\\"370000\\"}","fieldJBXXjgq":"371121","fieldJBXXjgq_Name":"五莲县","fieldJBXXjgq_Attr":"{\\"_parent\\":\\"371100\\"}","fieldJBXXjgsjtdz":"","fieldJBXXjjlxr":"汤翠文","fieldJBXXjjlxrdh":"15953397996","fieldSTQKsfstbs":"1","fieldSTQKks":false,"fieldSTQKgm":false,"fieldSTQKfs":false,"fieldSTQKfl":false,"fieldSTQKhxkn":false,"fieldSTQKfx":false,"fieldSTQKqt":false,"fieldSTQKqtms":"","fieldSTQKfrtw":"36","fieldWXTS":"温馨提示：体温若超过37.3℃，请带好口罩至学校医务所复测！","fieldSTQKqtqksm":"","fieldSTQKdqstzk":"","fieldSTQKglsjrq":"","fieldSTQKglsjsf":"","fieldSTQKfrsjrq":"","fieldSTQKfrsjsf":"","fieldCXXXcxzt":"1","fieldCXXXjtzz":"370000","fieldCXXXjtzz_Name":"山东省","fieldCXXXjtzzs":"371100","fieldCXXXjtzzs_Name":"日照市","fieldCXXXjtzzs_Attr":"{\\"_parent\\":\\"370000\\"}","fieldCXXXjtzzq":"371121","fieldCXXXjtzzq_Name":"五莲县","fieldCXXXjtzzq_Attr":"{\\"_parent\\":\\"371100\\"}","fieldCXXXjtjtzz":"榉园","fieldCXXXfxxq":"1","fieldCXXXfxxq_Name":"南京校区","fieldCXXXssh":"","fieldCXXXdqszd":"","fieldCXXXcqwdq":"","fieldCXXXfxcfsj":"","fieldCXXXjtfsfj":false,"fieldCXXXjtfshc":false,"fieldCXXXjtfsdb":false,"fieldCXXXjtfspc":false,"fieldCXXXjtfslc":false,"fieldCXXXjtfsqt":false,"fieldCXXXjtfsqtms":"","fieldCXXXjtgjbc":"","fieldYQJLjrsfczbl":"2","fieldYQJLjrsfczbldqzt":"","fieldYQJLsfjcqtbl":"2","fieldCXXXsftjwh":"","fieldCXXXsftjhb":"2","fieldCXXXsftjhbss":"","fieldCXXXsftjhbss_Name":"","fieldCXXXsftjhbs":"","fieldCXXXsftjhbs_Name":"","fieldCXXXsftjhbs_Attr":"{\\"_parent\\":\\"\\"}","fieldCXXXsftjhbq":"","fieldCXXXsftjhbq_Name":"","fieldCXXXsftjhbq_Attr":"{\\"_parent\\":\\"\\"}","fieldCXXXsftjhbjtdz":"","fieldYC":"420000","fieldMQJCRxh":[1],"fieldMQJCRxm":[""],"fieldMQJCRlxfs":[""],"fieldMQJCRcjdd":[""],"fieldCNS":true,"_VAR_ENTRY_NAME":"学生健康状况申报","_VAR_ENTRY_TAGS":"学工部"}'''
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
r4 = s.get('https://sc.ftqq.com/SCU156261Taa91200284745d9a18bad93b3f08260a6013e84603625.send?text=每日打卡成功')
