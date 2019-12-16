from Ketqua import spider_results, usernamefb, passwordfb
import os
import json
from datetime import datetime

import subprocess

temp=''
def datenow():
    a = datetime.now()
    print(a)
    return(a.strftime("%d/%m/%Y"))


def mang(temp):
    if temp == "Trong":
        return ""
    tempstring = ""
    for i in range(len(temp)):
        tempstring = tempstring+temp[i]+'\u000A'
    return tempstring


def thongtin(temp):
    blank = '\u000A'
    thu = temp["Thu"]
    ngay = temp["Ngay"]
    sang = mang(temp["Sang"])
    chieu = mang(temp["Chieu"])
    toi = mang(temp["Toi"])
    note = mang(temp["GhiChu"])
    return(str(thu)+': '+str(ngay)+blank+blank+'Sáng: '+blank+str(sang)+blank+'Chiều : '+blank+str(chieu)+blank+'Tối: '+blank+str(toi)+blank+'Ghi Chú: '+blank+str(note))


def xulyngay():
    subprocess.call(['scrapy','runspider' ,'login','-o' ,'test.json', 'Ketqua.py'])#['scrapy', 'crawl', spider_name, "-o", "output.json"]
    with open("test.json") as items_file:
        temp= items_file.read()
        print(temp)
    json_temp = json.loads(temp)
    for i in range(len(json_temp)):
        pass
        if(json_temp[i]["Ngay"] == datenow()):
            return thongtin(json_temp[i])
        else:
            continue

