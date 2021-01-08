import pymssql
import pandas as pd
from pandas import DataFrame


def getData():
    conn = pymssql.connect(host='140.138.155.188', user='sa', password='ltlab1612b', database='finalproject1091')
    cur = conn.cursor()
    cur.execute('SELECT * FROM [dbo].[restaurant];')
    table = cur.fetchall()
    df = DataFrame(table, columns=['key','name','type','address','image','rank'])
    # file_title = 'C:/Users/user/Documents/1091雲端/finalproject/test.xlsx'
    # df.to_excel(file_title, index=False)
    
    cur.close()
    conn.close()
    return df