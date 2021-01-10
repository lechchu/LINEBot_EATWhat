import boto3
import json
import random
import urllib
# from pandas import DataFrame
from boto3.dynamodb.conditions import Key, Attr

class RestaurantData:

    def databaseConnect(self):

        self.dynamodb = boto3.resource('dynamodb')
        self.restable = self.dynamodb.Table('linebot_EATWhat_DB')
        self.usertable = self.dynamodb.Table('linebot_EATWhat_Users')



    def makeResFlex(self, resdatas):
        reslist = json.load(open('flexJson/restaurant_emptylist.json',"r",encoding="utf-8"))
        for resdata in resdatas:
            # print(resdata.iloc[i]['name'])          
            json_temp = json.load(open('flexJson/restaurant_template.json',"r",encoding="utf-8"))
            # return(json_temp)
            json_temp['hero']['url'] = resdata['resImage'] #res pic url
            json_temp['body']['contents'][0]['text']= resdata['resName'] #res name
            json_temp['body']['contents'][2]['contents'][1]['contents'][1]['text'] = resdata['resAddress'] #res add
            res_add = json_temp['body']['contents'][2]['contents'][1]['contents'][1]['text']
            json_temp['body']['contents'][2]['contents'][1]['contents'][1]['action']['uri']+=(urllib.parse.quote(res_add)+'/') #res add uri
            json_temp['body']['contents'][2]['contents'][0]['contents'][1]['text'] = resdata['resType'] #res type      

            reslist['contents'].append(json_temp)

        return reslist

    def getFlexByFilter(self, keyword, userid, header='resType'):

        #make the restuarant list in system same to user's
        self.updateUserResList(userid)
        temp = []
        for res in self.res_list:
            if res['resType'] == keyword:
                temp.append(res)

        count = 3
        if len(temp)<3:
            count = len(temp)

        #random get 3 or less restaurant being Flex Message  
        return self.makeResFlex(random.sample(temp, count))


    def updateUserResList(self, userId):

        #get user's own restaurant list
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
    


