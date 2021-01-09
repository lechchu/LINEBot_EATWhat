import json
import random
# from database import RestaurantData
from resdataprocess import RestaurantData
from flask import Flask
app = Flask(__name__)
from pathlib import Path

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

line_bot_api = LineBotApi('Sr+SS3zWK9lc1yWz77+TjFLCuoTyh+GdRjijWpPFs5o73MaDNW8BT4at11ZA2LQU3w3hbHf+PnjCXns7RdKAOlGuEXDTO73k8AnB4+AxMmrfHJkGwavU8if+Frit7MQiY6olTsQ7JtH98yYaQn3LLAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2ea8e88dd76c05294bf5bc6f66d4890f')

# res_template = json.load(open('flexjson/restaurant_template.json',"r",encoding="utf-8"))
# res_type = json.load(open('flexjson/restaurant_type.json',"r",encoding="utf-8"))



try:
    resData = RestaurantData()
except Exception as e :
    print(e)



@app.route("/main", methods=['POST'])
def main():
    with open('data.txt', 'w', encoding='utf-8') as of:
        of.write(str(request.get_json()))
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent)
def handle_message(event):

    mtype = event.message.type
    if mtype == 'text':
        mtext = event.message.text
        if mtext == '@text2':
            FLEXmessage = FlexSendMessage(alt_text="test", contents=resData.res_template)
            line_bot_api.reply_message(event.reply_token, FLEXmessage)
        elif mtext == '@幫我決定':  
            message = TextSendMessage(text = "請選擇餐廳種類。")  
            FLEXmessage = FlexSendMessage(alt_text="餐廳種類選擇", contents=resData.res_type)
            line_bot_api.reply_message(event.reply_token, FLEXmessage)
        elif mtext == '@正餐':
            # resFlex = makeResFlex(Fliter(header='type', text=mtext[1:], pick_n=3))
            FLEXmessage = FlexSendMessage(alt_text="正餐列表", contents=resData.getFlexByFilter(mtext[1:]))
            line_bot_api.reply_message(event.reply_token, FLEXmessage)   
        elif mtext == '@早餐':
            # resFlex = makeResFlex(Fliter(header='type', text=mtext[1:], pick_n=3))
            FLEXmessage = FlexSendMessage(alt_text="早餐列表", contents=resData.getFlexByFilter(mtext[1:]))
            line_bot_api.reply_message(event.reply_token, FLEXmessage)   
        elif mtext == '@點心':
            # resFlex = makeResFlex(Fliter(header='type', text=mtext[1:], pick_n=3))
            FLEXmessage = FlexSendMessage(alt_text="點心列表", contents=resData.getFlexByFilter(mtext[1:]))
            line_bot_api.reply_message(event.reply_token, FLEXmessage)   
    # elif mtype=='image':
        # line_bot_api.reply_message(event.reply_token, message)
        
            
if __name__ == '__main__':
    app.run()
