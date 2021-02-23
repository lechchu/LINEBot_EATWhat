from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, JoinEvent, MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
)
import json
import logging
import os
from eatwhat_backend import RestaurantData

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

line_bot_api = LineBotApi('Sr+SS3zWK9lc1yWz77+TjFLCuoTyh+GdRjijWpPFs5o73MaDNW8BT4at11ZA2LQU3w3hbHf+PnjCXns7RdKAOlGuEXDTO73k8AnB4+AxMmrfHJkGwavU8if+Frit7MQiY6olTsQ7JtH98yYaQn3LLAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2ea8e88dd76c05294bf5bc6f66d4890f')

resData = RestaurantData()

eatwhatkeyword = ['吃甚麼', '吃啥', '吃什麼']

def isKeyword(text):
    for key in eatwhatkeyword:
        if key in text:
            return True
    return False

def lambda_handler(event, context):
    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):

        userid = json.loads(str(event.source))[str(event.source.type)+'Id']
        
        mtext = event.message.text
        if mtext == '@教我用':
            FLEXmessage = FlexSendMessage(alt_text="test", contents=resData.res_template)
            line_bot_api.reply_message(event.reply_token, FLEXmessage)
        elif mtext == '@幫我決定' or isKeyword(mtext):  
            FLEXmessage = FlexSendMessage(alt_text="餐廳種類選擇", contents=resData.res_type)
            line_bot_api.reply_message(event.reply_token, FLEXmessage)
        elif mtext == '@正餐':
            FLEXmessage = FlexSendMessage(alt_text="正餐列表", contents=resData.getFlexByFilter(mtext[1:], userid))
            line_bot_api.reply_message(event.reply_token, FLEXmessage)   
        elif mtext == '@早餐':
            FLEXmessage = FlexSendMessage(alt_text="早餐列表", contents=resData.getFlexByFilter(mtext[1:], userid))
            line_bot_api.reply_message(event.reply_token, FLEXmessage)   
        elif mtext == '@點心':
            FLEXmessage = FlexSendMessage(alt_text="點心列表", contents=resData.getFlexByFilter(mtext[1:], userid))
            line_bot_api.reply_message(event.reply_token, FLEXmessage) 


    @handler.add(JoinEvent)
    def handle_join(event):
        gourpid = json.loads(str(event.source))[str(event.source.type)+'Id']
        resData.updateUserResList(gourpid)

    @handler.add(FollowEvent)
    def handle_follow(event):
        userid = json.loads(str(event.source))[str(event.source.type)+'Id']
        resData.updateUserResList(userid)        
    
    try:
        signature = event['headers']['x-line-signature']
        body = event['body']
        handler.handle(body, signature)
    except InvalidSignatureError:
        return {'statusCode': 400, 'body': 'InvalidSignature'}
    return {'statusCode': 200, 'body': 'OK'}