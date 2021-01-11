import boto3
import json
import random
import urllib
# from pandas import DataFrame
from boto3.dynamodb.conditions import Key, Attr

class RestaurantData:


    def databaseConnect(self):       
        self.dynamodb = boto3.resource('dynamodb', region_name="us-east-1", aws_access_key_id='ASIASAILT6CMECQJ5WGV', aws_secret_access_key='OS0Luqzi91ZGBGYK+eNSgxY/KAgA0pDlM7btphqr', aws_session_token='FwoGZXIvYXdzEOb//////////wEaDHsIdqpG4sZpsUzHeiLIAXkNQb5tyP5RPTVh2b9/y8W+7rLtGtj1bxMVB8DMXOra9MOI97dfCZE2lPU+ibkuyRhzDscYsqNPsYd6zq0Bq3vGOJwxKlZf83LNDH9NKlghdF+a7s6a+WD25ouvwI16aGUQiIO6p7V1sFhuo+lSnPh3TbXs1GqUFe1FoIpYnWs4LQznlkrR+N4qXSmtqpYouTp56Oy/qGocfKASNkupckfNqngvNmualLWGn+slYmwK2nXtF1ipn3wDWOC8CsTID97DjGhzO8nMKNm27/8FMi2144nLcGjm0pyH8k+x4a7nxcetpFtaBzHxeEmAd89wVWac9E0YM6cTNhYQXIo=')
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
            json_temp['body']['contents'][2]['contents'][1]['contents'][1]['action']['uri']+=urllib.parse.quote(res_add) #res add uri
            print(json_temp['body']['contents'][2]['contents'][1]['contents'][1]['action']['uri'])
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
