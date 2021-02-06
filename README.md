# NUIST_AutoDailyHealthReport
## 南京信息工程大学每日健康打卡自动化

### 用法
用之前先去-office2.nuist.edu.cn/infoplus/form/XNYQSB/start 这里提交，提交的时候抓doAction的包，找到formdata，然后把里面的常量改成以下变量

_VAR_URL":"http://e-office2.nuist.edu.cn/infoplus/form/'''+str(stepId)+'''/render"

_VAR_NOW_DAY":"'''+str(datetime.datetime.now().day)+'''

"_VAR_NOW":"'''+str(t2)+'''"

_VAR_STEP_NUMBER":"'''+str(stepId)+'''"

,"fieldSQSJ":'''+str(t2)+''',

配置好之后保存到Formdata里面，注意用三个单引号括起来

保存好输入用户名密码就可以了

可以用方糖的推送，具体的自己研究下吧

自动化可以用github的action，也可以用腾讯云函数，这个都可以
