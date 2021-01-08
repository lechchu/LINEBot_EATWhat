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
    reslist = json.load(open('flexjson/restaurant_emptylist.json',"r",encoding="utf-8"))
    for i in range(len(resdata)):
        print(resdata.iloc[i]['name'])
        djson = json.load(open('flexjson/restaurant_template.json',"r",encoding="utf-8"))

        djson['hero']['url'] = resdata.iloc[i]['image'] #res pic url
        djson['body']['contents'][0]['text']= resdata.iloc[i]['name'] #res name
        djson['body']['contents'][2]['contents'][1]['contents'][1]['text'] = resdata.iloc[i]['address'] #res add
        res_add = djson['body']['contents'][2]['contents'][1]['contents'][1]['text']
        djson['body']['contents'][2]['contents'][1]['contents'][1]['action']['uri']+=res_add #res add uri
        djson['body']['contents'][2]['contents'][0]['contents'][1]['text'] = resdata.iloc[i]['type'] #res type
        reslist['contents'].append(djson)
    
    # print(json['body']['contents'][2]['contents'][0]['contents'][1]['text']) #res name
    print(reslist)
    return reslist


def Fliter(header, text, pick_n):
    fliter = (df[header] == text)
    return (df[fliter].sample(n=pick_n))






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
            FLEXmessage = FlexSendMessage(alt_text="test", contents=res_template)
            line_bot_api.reply_message(event.reply_token, FLEXmessage)
        elif mtext == '@幫我決定':  
            message = TextSendMessage(text = "請選擇餐廳種類。")  
            FLEXmessage = FlexSendMessage(alt_text="餐廳種類選擇", contents=res_type)
            line_bot_api.reply_message(event.reply_token, FLEXmessage)
        elif mtext == '@正餐':
            resFlex = makeResFlex(Fliter(header='type', text=mtext[1:], pick_n=3))
            FLEXmessage = FlexSendMessage(alt_text="正餐列表", contents=resFlex)
            line_bot_api.reply_message(event.reply_token, FLEXmessage)   
        elif mtext == '@早餐':
            resFlex = makeResFlex(Fliter(header='type', text=mtext[1:], pick_n=3))
            FLEXmessage = FlexSendMessage(alt_text="早餐列表", contents=resFlex)
            line_bot_api.reply_message(event.reply_token, FLEXmessage)   
        elif mtext == '@點心':
            resFlex = makeResFlex(Fliter(header='type', text=mtext[1:], pick_n=3))
            FLEXmessage = FlexSendMessage(alt_text="點心列表", contents=resFlex)
            line_bot_api.reply_message(event.reply_token, FLEXmessage)   
    # elif mtype=='image':
        # line_bot_api.reply_message(event.reply_token, message)
        
            
if __name__ == '__main__':
    app.run()
