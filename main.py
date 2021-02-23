import json
import random
from eatwhat_backend import RestaurantData
from flask import Flask
app = Flask(__name__)
from pathlib import Path

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

line_bot_api = LineBotApi('jvCTs7FaFprc2fcx6T7ISlu0l91s5pjP4HoR74B73bqjNqCICAM3PZTknhPNsIXjd0k0QdsT+yzql/M0LBZJKoW/nG62d3VkSOq0Z59UzVqyS+Yyr5tYJXiMDYFueicCGF1cm+IsqFpMb5YcT9kAdQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d5660aa241d5041e268c14cf6d8b0fb4')

eatwhatkeyword = ['吃甚麼', '吃啥', '吃什麼']

try:
    resData = RestaurantData()
except Exception as e :
    print(e)

def isKeyword(text):
    for key in eatwhatkeyword:
        if key in text:
            return True
    return False


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
    userid = json.loads(str(event.source))[str(event.source.type)+'Id']
    
    if mtype == 'text':
        
        mtext = event.message.text

        if mtext == '@text':
            # message = TextSendMessage(text='aa')
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = str(event.type)))
        elif mtext == '@幫我決定' or isKeyword(mtext):  
            message = TextSendMessage(text = "請選擇餐廳種類。")  
            FLEXmessage = FlexSendMessage(alt_text="餐廳種類選擇", contents=resData.res_type)
            line_bot_api.reply_message(event.reply_token, FLEXmessage)
        elif mtext == '@正餐':
            FLEXmessage = FlexSendMessage(alt_text="正餐列表", contents=resData.getFlexByFilter(mtext[1:], userid))
            line_bot_api.reply_message(event.reply_token, FLEXmessage)
    # elif mtype=='image':
        # line_bot_api.reply_message(event.reply_token, message)

@handler.add(JoinEvent)
def handle_join(event):
    gourpid = json.loads(str(event.source))[str(event.source.type)+'Id']
    resData.updateUserResList(gourpid)

@handler.add(FollowEvent)
def handle_follow(event):
    userid = json.loads(str(event.source))[str(event.source.type)+'Id']
    resData.updateUserResList(userid)

if __name__ == '__main__':
    app.run(debug=True)
