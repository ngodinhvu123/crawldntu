from flask import Flask, request
import json
import requests
import chatbot
app = Flask(__name__)
VERIFY_TOKEN = '@thaonguyen'
FB_API_URL = 'https://graph.facebook.com/v5.0/me/messages'
PAGE_ACCESS_TOKEN = 'EAAVJSnewzxkBANcGJI7vkRHMR4N6ZCCbRWiqHU9SFRlTNNouIZCv9yP2rR4xHl5MVmJZBjlgN2MRqnpZCXjdHZAsJkLEujyAOdSGJhqo3vYQ5vy1NXRMevbgURB6ZCZCuuJtIXsSAEA24xkmyCAGTFknUY76BP6MVOb6vb9Aj7Yj5eKQbRW7phpvnv83eaXJY8ZD'


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
    messaging = ((data["entry"][0]["messaging"]))
    return(messaging[0]["message"]["text"])


def id_replace(data):
    id_user = data["entry"][0]["messaging"][0]["sender"]["id"]
    return id_user


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
    data = request.get_json()
    if showmess(data)=='tkb':
        try:
            print(send_message(id_replace(data), chatbot.xulyngay()))
        except:
            print("loi")
    else:
        print(send_message(id_replace(data),'sai cú pháp'))
    return data


if __name__ == "__main__":
    app.run(debug=True)
