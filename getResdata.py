import boto3
import json
import random
# from pandas import DataFrame
from boto3.dynamodb.conditions import Key, Attr

class RestaurantData:


    def databaseConnect(self):       
        self.dynamodb = boto3.resource('dynamodb', region_name="us-east-1", aws_access_key_id='ASIASAILT6CMMIJPYN7T', aws_secret_access_key='Q4I/makAw7vVWKutjLRGF6FIRHfjApFePn4SJ5v3', aws_session_token='FwoGZXIvYXdzENz//////////wEaDD68UDM63DYrW6eRISLIAdA9GLe4ZnT/Gk727qUjXij8ROQyjw66FHXsSrPRwrheBiDdgiMm/jhBSSyXTLu8R52pwT/zl07rfjjnzsdj02Znw6gTHffcQxRiueSk2fiZdf7z03+XqO6kasR9NR+/55JH4EyX0PcZHQFOiZ3yOkQIG+oIVVviF4HMZvYQnI9HhHeNExrI+4b7aD4dAeBBxyrPr7PET2L5vuqZB5GCa2HlP5DujP3ZdAKgkwPN0C+v0ejAfLAg2dG00E9iIG3UYMcAYi7uSezPKIyY7f8FMi0sLLUZExdaOq7pB9r3cddYdfGXXT1wa158yIrsdTq31QnMV/Lr2bRwSr5G/UU=')
        self.restable = self.dynamodb.Table('linebot_EATWhat_DB')
        self.usertable = self.dynamodb.Table('linebot_EATWhat_Users')


    def makeResFlex(self, resdatas):
        reslist = json.load(open('flexJson/restaurant_emptylist.json',"r",encoding="utf-8"))
        for resdata in resdatas:
            # print(resdata.iloc[i]['name'])          
            json_temp = json.load(open('flexJson/restaurant_template.json',"r",encoding="utf-8"))
            json_temp['hero']['url'] = resdata['resImage'] #res pic url
            json_temp['body']['contents'][0]['text']= resdata['resName'] #res name
            json_temp['body']['contents'][2]['contents'][1]['contents'][1]['text'] = resdata['resAddress'] #res add
            res_add = json_temp['body']['contents'][2]['contents'][1]['contents'][1]['text']
            json_temp['body']['contents'][2]['contents'][1]['contents'][1]['action']['uri']+=res_add #res add uri
            json_temp['body']['contents'][2]['contents'][0]['contents'][1]['text'] = resdata['resType'] #res type      

            reslist['contents'].append(json_temp)
            # json_temp.clear()

        return reslist

    def getFlexByFilter(self, keyword, userid, header='resType'):

        self.updateUserResList(userid)
        temp = []
        for res in self.res_list:
            if res['resType'] == keyword:
                temp.append(res)

        count = 3
        if len(temp)<3:
            count = len(temp)
        return self.makeResFlex(random.sample(temp, count))


    def updateUserResList(self, userId):
        self.user_reslist = self.usertable.query(
        KeyConditionExpression=Key('userId').eq(userId)
        )

        #if user not in database, init the data 
        if self.user_reslist['Count'] == 0:
            user_reslist = []
            for i in range(len(self.res_list)):             
                user_reslist.append(int(self.res_list[i]['resID']))

            self.usertable.put_item(       
                Item={
                'userId': userId,
                'resList': user_reslist
                }
            )

        # make reslist to user own reslist
        self.user_reslist = self.user_reslist['Items'][0]['resList']

        temp =[]
        for i in range(len(self.res_list)):
            if int(self.res_list[i]['resID']) in self.user_reslist:               
                temp.append( self.res_list[i])
        self.res_list = temp

        

    def __init__(self):
        self.databaseConnect()
        self.res_list = self.restable.scan()['Items']
        self.user_reslist = self.res_list
        self.res_template = json.load(open('./flexJson/restaurant_template.json',"r",encoding="utf-8"))
        self.res_type = json.load(open('./flexJson/restaurant_type.json',"r",encoding="utf-8"))
    


RestaurantData()
