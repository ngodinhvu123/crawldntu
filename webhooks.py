from flask import Flask, request
import json
import requests
import chatbot
import os
app = Flask(__name__)
VERIFY_TOKEN = '@thaonguyen'
FB_API_URL = 'https://graph.facebook.com/v5.0/me/messages'
PAGE_ACCESS_TOKEN = 'EAAVJSnewzxkBAEPvZArsPw3Y7R2WvocuukAnpHTiNZBdywPIO4JESkeraVJz1c8vXgu1ZCtxTlbtZCZAsMpZBZBTiSB4YYUzwVfmsU4QTdX1ZBJBNrCwxvXktrOSd93jxtKj147U6XjysbOFDsklgVNWEMrLUydelJ28chC1K2yPVpXlrrkZA9RKO8JTeUTlUtyAZD'

count=0
checkmk=False
tk=''
mk=''
def send_message(recipient_id, text):
    """Send a response to Facebook"""
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({"recipient": {
        "id": recipient_id
    },
        "message": {
        "text": text
    }})
    print(data)
    r = requests.post("https://graph.facebook.com/v5.0/me/messages",params=params, headers=headers, data=data)

    return r.json()


def showmess(data):
    try:
        messaging = ((data["entry"][0]["messaging"]))
        return(messaging[0]["message"]["text"])
    except :
        return "loi messaging"


def id_replace(data):
    try:
        id_user = data["entry"][0]["messaging"][0]["sender"]["id"]
        return id_user
    except:
        return "loi lay id"


def laytkmk(data):
    send_message(id_replace(data),"nhập mssv: ")
    tk=showmess(data)
    send_message(id_replace(data),"nhập mk: ")
    mk=showmess(data)

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    global count,tk,mk
    data = request.get_json()
    try:
        if showmess(data)=='tkb':
            send_message(id_replace(data),"Đang xử lý"+"Buoc:"+str(count+1))
            send_message(id_replace(data),"moi nhap mssv: ")
            count=1
        elif (showmess(data)).isdigit() and count==1:
            send_message(id_replace(data),"Đang xử lý"+"Buoc:"+str(count+1))
            send_message(id_replace(data),"moi nhap mat khau")   
            tk=showmess(data)
            count=0
        elif count!=1 :
            mk=showmess(data)      
            if tk!='' and mk!='':
                mk=showmess(data)
                send_message(id_replace(data),"Đang xử lý")
                try:    
                    send_message(id_replace(data),chatbot.xulyngay(tk,mk))
                    count=0;tk='';mk=''
                except :
                    send_message(id_replace(data),"lỗi trong quá trình lấy thời khóa biểu")
                    count=0;tk='';mk=''
            
    except Exception as e:
        send_message(id_replace(data),"loi nguyen trong")
        print(e)
    return data


if __name__ == "__main__":
    app.run()
