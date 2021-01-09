import pymssql
import json
import pandas as pd
from pandas import DataFrame


class RestaurantData:

    def databaseConnect(self):
        conn = pymssql.connect(host='140.138.155.188', user='sa', password='ltlab1612b', database='finalproject1091')
        cur = conn.cursor()
        cur.execute('SELECT * FROM [dbo].[restaurant];')
        table = cur.fetchall()
        self.restaurantDF = DataFrame(table, columns=['resID','name','type','address','image','rank'])
        result = self.restaurantDF.to_json(orient="table")
        parsed = json.loads(result)
        json.dumps(parsed, indent=4)  
        cur.close()
        conn.close()


    def makeResFlex(self, resdata):
        reslist = json.load(open('flexjson/restaurant_emptylist.json',"r",encoding="utf-8"))
        for i in range(len(resdata)):
            # print(resdata.iloc[i]['name'])
            
            json_temp = json.load(open('flexjson/restaurant_template.json',"r",encoding="utf-8"))
            json_temp['hero']['url'] = resdata.iloc[i]['image'] #res pic url
            json_temp['body']['contents'][0]['text']= resdata.iloc[i]['name'] #res name
            json_temp['body']['contents'][2]['contents'][1]['contents'][1]['text'] = resdata.iloc[i]['address'] #res add
            res_add = json_temp['body']['contents'][2]['contents'][1]['contents'][1]['text']
            json_temp['body']['contents'][2]['contents'][1]['contents'][1]['action']['uri']+=res_add #res add uri
            json_temp['body']['contents'][2]['contents'][0]['contents'][1]['text'] = resdata.iloc[i]['type'] #res type      

            reslist['contents'].append(json_temp)
            # json_temp.clear()
        return reslist

    def getFlexByFilter(self, keyword, header='type'):
        fliter = (self.restaurantDF[header] == keyword)
        resDF = self.restaurantDF[fliter].sample(n=3)
        return self.makeResFlex(resDF)

    def __init__(self):
        self.databaseConnect()
        self.res_template = json.load(open('flexjson/restaurant_template.json',"r",encoding="utf-8"))
        self.res_type = json.load(open('flexjson/restaurant_type.json',"r",encoding="utf-8"))
    

conn = pymssql.connect(host='140.138.155.188', user='sa', password='ltlab1612b', database='finalproject1091')
cur = conn.cursor()
cur.execute('SELECT * FROM [dbo].[restaurant];')
table = cur.fetchall()
restaurantDF = DataFrame(table, columns=['resID','name','type','address','image','rank'])
restaurantDF.to_csv('./data.csv', index=False)
# result = restaurantDF.to_json(orient="table")
# parsed = json.loads(result)
# print(json.dumps(parsed, indent=4, ensure_ascii=False))  
cur.close()
conn.close()

