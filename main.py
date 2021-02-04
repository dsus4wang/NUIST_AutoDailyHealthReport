# -*- coding: UTF-8 -*-
import requests
import time
from bs4 import BeautifulSoup
import datetime
import json
from urllib.parse import urlencode
import urllib

iPDP=input("iPlanetDirectoryPro")
formDatainp=input("formData2")


s = requests.Session()
url = 'http://e-office2.nuist.edu.cn/infoplus/form/XNYQSB/start'
# cookies = dict(INGRESSCOOKIE='1612425402.576.120.251848', JSESSIONID='1C75229FB4005E181C8DAAF8857AB3FA.TomcatC',iPlanetDirectoryPro='Xdu0h0zdQlig2dtROU3fee7rhZx0lYJh')
cookies = dict(iPlanetDirectoryPro=iPDP)
r1 = s.get(url,cookies=cookies)
cookieNew = r1.cookies
htmlTextOri = r1.text
html = BeautifulSoup(htmlTextOri,'lxml')
print(html)
tar1 = str(html.find_all('meta')[3])
csrfToken = tar1.split('"')[1]
url2 = 'http://e-office2.nuist.edu.cn/infoplus/interface/start'
data2 = {'idc':'XNYQSB',
         'release':'',
         'csrfToken':csrfToken,
         'formData':'{"_VAR_URL":"http://e-office2.nuist.edu.cn/infoplus/form/XNYQSB/start","_VAR_URL_Attr":"{}"}'
        }
header2 = {'Referer':'http://e-office2.nuist.edu.cn/infoplus/form/XNYQSB/start' ,
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
           'Origin': 'http://e-office2.nuist.edu.cn',
           }
r2 = s.post(url2, data = data2 , cookies=cookieNew,headers=header2)
print(r2.text)
targetUrl = json.loads(r2.text)['entities'][0]
stepId = int(targetUrl.split('/')[5])
t2 = int(time.time())
formData2 = formDatainp
postData2={
    'actionId':1,
    'formData' : formData2,
    'remark':'',
    'rand': 185.43415117494698,
    'nextUsers':'{}',
    'stepId':stepId,
    'timestamp':t2,
    'boundFields':'fieldCXXXjtgjbc,fieldMQJCRxh,fieldCXXXsftjhb,fieldSTQKqt,fieldSTQKglsjrq,fieldYQJLjrsfczbldqzt,fieldCXXXjtfsqtms,fieldCXXXjtfsfj,fieldJBXXjjlxrdh,fieldJBXXxm,fieldJBXXjgsjtdz,fieldCXXXsftjhbss,fieldSTQKfrtw,fieldMQJCRxm,fieldCXXXsftjhbq,fieldSTQKqtms,fieldCXXXjtfslc,fieldJBXXlxfs,fieldJBXXxb,fieldCXXXjtfspc,fieldYQJLsfjcqtbl,fieldCXXXssh,fieldJBXXgh,fieldCNS,fieldYC,fieldSTQKfl,fieldCXXXsftjwh,fieldCXXXfxxq,fieldSTQKdqstzk,fieldSTQKhxkn,fieldSTQKqtqksm,fieldFLid,fieldYQJLjrsfczbl,fieldJBXXjjlxr,fieldCXXXfxcfsj,fieldMQJCRcjdd,fieldSQSJ,fieldSTQKfrsjrq,fieldSTQKks,fieldJBXXcsny,fieldSTQKgm,fieldJBXXnj,fieldCXXXjtzzq,fieldJBXXJG,fieldCXXXdqszd,fieldCXXXjtzzs,fieldSTQKfx,fieldSTQKfs,fieldCXXXjtfsdb,fieldCXXXcxzt,fieldCXXXjtfshc,fieldCXXXjtjtzz,fieldCXXXsftjhbs,fieldJBXXsfzh,fieldSTQKsfstbs,fieldCXXXcqwdq,fieldJBXXfdygh,fieldJBXXjgshi,fieldJBXXfdyxm,fieldWXTS,fieldCXXXjtzz,fieldJBXXjgq,fieldCXXXjtfsqt,fieldJBXXjgs,fieldSTQKfrsjsf,fieldSTQKglsjsf,fieldJBXXdw,fieldCXXXsftjhbjtdz,fieldMQJCRlxfs',
    'csrfToken':csrfToken,
    'lang':'zh',
}

url3 = 'http://e-office2.nuist.edu.cn/infoplus/interface/doAction'
header3 = {'Referer':'http://e-office2.nuist.edu.cn/infoplus/form/'+str(stepId)+'/render' ,
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
           'Origin': 'http://e-office2.nuist.edu.cn',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          }
r3 = s.post(url3, data = postData2 , cookies=cookieNew,headers=header3)
print(r3.text)
