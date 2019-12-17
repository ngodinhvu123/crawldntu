import os
import json
from datetime import datetime
from pytz import timezone
import subprocess
import Ketqua
temp=''
def datenow():
    a = datetime.now().astimezone(timezone('Asia/Ho_Chi_Minh'))
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


def xulyngay(mssv,mk):
    ms_sv='mssv='+mssv
    m_k='mk='+mk
    print(ms_sv)
    subprocess.call(['scrapy','runspider', 'Ketqua.py', '-a',ms_sv, '-a', m_k,'-o', 'test.json'])
    with open("test.json") as items_file:
        temp= items_file.read()
    os.remove('test.json')
    json_temp = json.loads(temp)
    for i in range(len(json_temp)):
        if(json_temp[i]["Ngay"] == datenow()):
            return thongtin(json_temp[i])
        else:
            continue