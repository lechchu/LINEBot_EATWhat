import json
import random
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
        if mtext == '@text':
            FLEXmessage = FlexSendMessage(alt_text="農產品選擇", contents=res_template)
            line_bot_api.reply_message(event.reply_token, FLEXmessage)
        elif mtext == '@text2':  
            message = TextSendMessage(text = "請選擇餐廳種類。")  
            FLEXmessage = FlexSendMessage(alt_text="餐廳種類選擇", contents=res_type)
            line_bot_api.reply_message(event.reply_token, message)
        elif mtext == '@查看訂購流程':  
            FLEXmessage = FlexSendMessage(alt_text="訂購流程", contents=useflowFlex)
            line_bot_api.reply_message(event.reply_token, FLEXmessage)   
        elif mtext == '@營養蔬菜':
            FLEXmessage = FlexSendMessage(alt_text="營養蔬菜種類", contents=vegetablesFlex)
            line_bot_api.reply_message(event.reply_token, FLEXmessage)
        elif mtext == '@來來平價水果地址':
            message = LocationMessage(title='來來平價水果',address='台北市大安區辛亥路一段103號', latitude=25.0220311, longitude=121.5313405)
            line_bot_api.reply_message(event.reply_token, message)
    elif mtype=='image':
        # message = TextSendMessage(text = '我們認為這顆芒果的等級會是: \n'+mangoLevel[random.randint(0,2)])
        message = TextSendMessage(text = '我們認為這顆芒果的等級會是: \n'+mangoLevel[1])
        line_bot_api.reply_message(event.reply_token, message)
        
            
if __name__ == '__main__':
    app.run()
