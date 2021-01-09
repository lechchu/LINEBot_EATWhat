import boto3
import json
import random
# from pandas import DataFrame
from boto3.dynamodb.conditions import Key, Attr

class RestaurantData:

    def databaseConnect(self):

        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('linebot_EATWhat_DB')



    def makeResFlex(self, resdatas):
        reslist = json.load(open('flexJson/restaurant_emptylist.json',"r",encoding="utf-8"))
        for resdata in resdatas:
       
            json_temp = json.load(open('flexJson/restaurant_template.json',"r",encoding="utf-8"))
            json_temp['hero']['url'] = resdata['resImage'] #res pic url
            json_temp['body']['contents'][0]['text']= resdata['resName'] #res name
            json_temp['body']['contents'][2]['contents'][1]['contents'][1]['text'] = resdata['resAddress'] #res add
            res_add = json_temp['body']['contents'][2]['contents'][1]['contents'][1]['text']
            json_temp['body']['contents'][2]['contents'][1]['contents'][1]['action']['uri']+=res_add #res add uri
            json_temp['body']['contents'][2]['contents'][0]['contents'][1]['text'] = resdata['resType'] #res type      

            reslist['contents'].append(json_temp)

        return reslist

    def getFlexByFilter(self, keyword, header='resType'):

        response = self.table.scan(
            FilterExpression=Attr(header).eq(keyword)
            # , Limit=4
        )
        return self.makeResFlex(random.sample(response['Items'], 3))

    def __init__(self):
        self.databaseConnect()
        self.res_template = json.load(open('./flexJson/restaurant_template.json',"r",encoding="utf-8"))
        self.res_type = json.load(open('./flexJson/restaurant_type.json',"r",encoding="utf-8"))
    


