import json
import random
from database import getData
from flask import Flask
app = Flask(__name__)
from pathlib import Path

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

line_bot_api = LineBotApi('Sr+SS3zWK9lc1yWz77+TjFLCuoTyh+GdRjijWpPFs5o73MaDNW8BT4at11ZA2LQU3w3hbHf+PnjCXns7RdKAOlGuEXDTO73k8AnB4+AxMmrfHJkGwavU8if+Frit7MQiY6olTsQ7JtH98yYaQn3LLAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2ea8e88dd76c05294bf5bc6f66d4890f')

res_template = json.load(open('flexjson/restaurant_template.json',"r",encoding="utf-8"))
res_type = json.load(open('flexjson/restaurant_type.json',"r",encoding="utf-8"))

print(res_template['hero']['url'])#res pic url
print(res_template['body']['contents'][0]['text'])#res name
res_add = res_template['body']['contents'][2]['contents'][1]['contents'][1]['text']
print(res_template['body']['contents'][2]['contents'][1]['contents'][1]['text'])#res add
print(res_template['body']['contents'][2]['contents'][1]['contents'][1]['action']['uri']+res_add)#res add uri
print(res_template['body']['contents'][2]['contents'][0]['contents'][1]['text'])#res type

try:
    df = getData()
except Exception as e :
    print(e)

def makeResFlex(resdata):
    json = res_template
    print(json['body']['contents'][2]['contents'][0]['contents'][1]['text']) #res name
    return json


def Fliter(header, text, pick_n):
    fliter = (df[header] == text)
    print(df[fliter].sample(n=pick_n))
    return (df[fliter].sample(n=pick_n))

def selfPrint(text):
    print(text)


# useflowFlex = json.load(open('FLEXJson/useflow_BubbleFLEX.json',"r",encoding="utf-8"))
# fruitsFlex = json.load(open('FLEXJson/layer3_fruits.json',"r",encoding="utf-8"))
# vegetablesFlex = json.load(open('FLEXJson/layer3_vegetables.json',"r",encoding="utf-8"))
# grainsFlex = json.load(open('FLEXJson/layer3_grains.json',"r",encoding="utf-8"))
# persimmonNear = json.load(open('FLEXJson/persimmonNear_FLEX.json',"r",encoding="utf-8"))
# persimmonOnline = json.load(open('FLEXJson/persimmonOnline_FLEX.json',"r",encoding="utf-8"))
# tomatoNear = json.load(open('FLEXJson/tomatoNear_FLEX.json',"r",encoding="utf-8"))
# tomatoOnline = json.load(open('FLEXJson/tomatoOnline_FLEX.json',"r",encoding="utf-8"))
# peanutNear = json.load(open('FLEXJson/peanutNear_FLEX.json',"r",encoding="utf-8"))
# peanutOnline = json.load(open('FLEXJson/peanutOnline_FLEX.json',"r",encoding="utf-8"))

@app.route("/main", methods=['POST'])
def main():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# TODO 
# 結帳頁面的購買者資訊自動填入(藉由擷取LIFF特性 LINE Login資訊)
# 調整ifelse結構

@handler.add(MessageEvent)
def handle_message(event):
    mtype = event.message.type
    if mtype == 'text':
        mtext = event.message.text
        if mtext == '@text2':
            FLEXmessage = FlexSendMessage(alt_text="農產品選擇", contents=res_template)
            line_bot_api.reply_message(event.reply_token, FLEXmessage)
        elif mtext == '@幫我決定':  
            selfPrint('aaa')
            message = TextSendMessage(text = "請選擇餐廳種類。")  
            FLEXmessage = FlexSendMessage(alt_text="餐廳種類選擇", contents=res_type)
            line_bot_api.reply_message(event.reply_token, FLEXmessage)
        elif mtext == '正餐':
            print('111')
            selfPrint(mtext)
            Fliter(header='type', text=mtext, pick_n=5)
            # message = TextSendMessage(text = str(Fliter(header='type', text=mtext, pick_n=5)['name'][0]))
            # FLEXmessage = FlexSendMessage(alt_text="正餐列表", contents=makeResFlex())
            # line_bot_api.reply_message(event.reply_token, message)   
        # elif mtext == '@早餐':
        #     FLEXmessage = FlexSendMessage(alt_text="早餐列表", contents=makeResFlex())
        #     line_bot_api.reply_message(event.reply_token, FLEXmessage)
        # elif mtext == '@點心':
        #     FLEXmessage = FlexSendMessage(alt_text="點心列表", contents=makeResFlex())
        #     line_bot_api.reply_message(event.reply_token, FLEXmessage)
    elif mtype=='image':
        # message = TextSendMessage(text = '我們認為這顆芒果的等級會是: \n'+mangoLevel[random.randint(0,2)])
        message = TextSendMessage(text = '我們認為這顆芒果的等級會是: \n'+mangoLevel[1])
        line_bot_api.reply_message(event.reply_token, message)
        
            
if __name__ == '__main__':
    app.run()
