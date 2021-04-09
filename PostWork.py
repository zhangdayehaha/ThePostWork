"""
#
#by TheWarmHearted
#
"""

import os
import requests
import time
from PIL import Image
import pytesseract
import re
#伪装headers躲过服务器--获取认证--下载验证码--学习识别-提交表单--访问服务器-添加加班表

Rusturl='加班'
TheWorkNum='107266'
TheWorkNumKey='z18753015421'
TheWorkNumS='200341'
#print(os.getcwd())
try:
 with open(os.getcwd()+'\\''config.ini','r') as f:
     Rusturl=f.read()
except Exception as err:
        print(repr(err))
        input()
print(Rusturl)
config=Rusturl.split('\n')
Rusturl=config[0][3:]
TheWorkNum=config[1][3:]
TheWorkNumKey=config[2][3:]
TheWorkNumS = config[3]
if '二' in config[3]:
    TheWorkNumS='200341'
elif '一' in config[3]:
    TheWorkNumS='200308'
print(Rusturl,TheWorkNum,TheWorkNumKey,TheWorkNumS)
#input('changshi')
Rus=Rusturl.encode("unicode_escape").decode('UTF-8')
Rus=str(Rus).replace("\\","%")
ming=time.strftime('%Y/%m/%d',time.localtime(time.time()))
TheTime=time.strftime('%H-%M-%S',time.localtime(time.time()))

def code_riz(res):
    BMP=res.content
    with open('code.bmp','wb') as f:
        f.write(BMP)

    pic = Image.open('code.bmp')
    pic = pic.resize((700, 260),Image.BICUBIC    )

    Img = pic.convert('L')
    Img.save('1.bmp')
    threshold = 200

    table = []
    for i in range(256):
        if i >186:
            table.append(0)
        else:
            table.append(1)

    photo = Img.point(table, '1')

    p = Image.new('RGBA', (1000,1000), (255,255,255))

    p.paste(photo, (100, 100) ,None)
    p.save('11.bmp')
def get_cookie():
    url_code='http://192.168.28.228:7108/BS_login.asp'
    URL_CODE='http://192.168.28.228:7108/yy_select/yy_login.asp'


    headers = {
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Cache-Control': 'max-age=0',
               'Upgrade-Insecure-Requests': '1'
               }
    headers_code={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    }
    s = requests.Session()
    res = s.get(URL_CODE, headers=headers)

    cookies = requests.utils.dict_from_cookiejar(res.cookies)
    for i in cookies:
        tou=i
        break
    
    #input(cookies[tou])    
    headers_code['Cookie']=tou+'='+ str(cookies[tou])
    
    ##print(headers_code['Cookie'])
    return headers_code
SysStart=0
while True:
    try:
        TheTime=time.strftime('%H-%M-%S',time.localtime(time.time()))
        #print(TheTime,SysStart)
        if SysStart ==0 or TheTime =='8-10-03':
            
            s = requests.Session()
            #获取服务器端建立的token跟cookies，过验证
            Hearders=get_cookie()
            res = s.get('http://192.168.28.228:7108/default.asp', headers=Hearders)

            params={'u_1':'cn',
                    'u_2':'yyyy/MM/dd',
                    'u_3':'0'
                    }
            res = s.post('http://192.168.28.228:7108/yy_select/yy_default.asp', data=params,headers=Hearders)
            params={'u_1':''}
            res = s.post('http://192.168.28.228:7108/yy_select/yy_login.asp', data=params,headers=Hearders)

            urlcocde='http://192.168.28.228:7108/yy_oledb/yy_validate.asp'#JOSN网址验证码获取

            res = s.post(urlcocde, headers=Hearders)
            code_riz(res)

            #机器学习识别的图像的字符串
            bbb=pytesseract.image_to_string(Image.open('11.bmp'))

            ccc=''
            for i in re.findall('[0-9]',bbb):

                ccc=ccc+i
            ##print(ccc)


            code=TheWorkNum+'|-|'+TheWorkNumKey+'|-|'+ccc+'|-|'
            params3={'user_no':TheWorkNum,
                           'user_pass':TheWorkNumKey,
                           'user_vali':ccc,
                           'Impress_form':code
                            }
            #把验证码提交
            url='http://192.168.28.228:7108/yy_login/yy3667_main.asp'#登录表单网址
            res = s.post(url,data=params3,headers=Hearders)#登录
            
            url='http://192.168.28.228:7108/yy_select/yy_dowhere.asp'
            res = s.post(url,headers=Hearders)#登录

            res.encoding = "UTF-8"
            #print(res.text)
            #print(re.findall('3D(.*?)%',res.text))
            
            IDN=re.findall('3D(.*?)%',res.text)
            params3={
                     'kssj':ming,
                     'bz':Rusturl,
                     's_bh':'',
                     'Impress_form':Rus+'|-|'+ming+'|-|'+IDN[0]+'|-|0|-|0|-|1'
                    }
            #提交加班理由以及日期过验证
            res = s.post('http://192.168.28.228:7108/bus_apply/yy3667_main.asp',data=params3,headers=Hearders)#获取列表

            html = res.text
            print(html)

            #查询是否成功
            
            #params3={'u_3':'20003156'}
            #res = s.post('http://192.168.28.228:7108/bus_apply/yy3664_main.asp',params=params3,headers=Hearders)#获取列表
            res = s.get('http://192.168.28.228:7108/yy_dep/yy3677_main.asp',headers=Hearders)#获取列表
            res = s.get('http://192.168.28.228:7108/main_xml/tree/YY.YY3-668.asp',headers=Hearders)#获取列表
            res = s.get('http://192.168.28.228:7108/bus_apply/yy3668_main.asp',headers=Hearders)#获取列表
            res = s.get('http://192.168.28.228:7108/bus_apply/yy3665_main.asp',headers=Hearders)#获取列表

            params3={'v_0':'',
                     'v_2':'M6216',
                     'u_0':'null',
                     'u_1':'null',
                     'u_2':'null',
                     'u_3':'%28b.dep_no%20is%20not%20null%20and%20b.user_serial%3D'+IDN[0]+'%29%20and%20a.over_date%3D%27'+ming+'%27%20and%20%28b.user_dep%3D'+TheWorkNumS+'%29',
                     'u_4':'null',
                     'u_5':'null',
                     'v_1':'0',
                    }
            
            res = s.post('http://192.168.28.228:7108/main_xml/dgrid/YY.YY3-668.asp',data=params3,headers=Hearders)#获取列表
            params3['v_1']='1'
            res = s.post('http://192.168.28.228:7108/main_xml/dgrid/YY.YY3-668.asp',data=params3,headers=Hearders)#获取列表

            res.encoding = "UTF-8"
            html = res.text
            print(html)
            reust=re.findall(Rusturl,html)
            
            if reust:
                SysStart=1
                #input()
                #print(reust)
                break
            else:
                #break
                pass
                ##print(html)
    except Exception as err:
        pass
        
            #print(repr(err))
