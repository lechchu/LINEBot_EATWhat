import pymssql
import pandas as pd
from pandas import DataFrame

def Fliter(df, header, text, pick_n):
    fliter = (df[header] == text)
    print(df[fliter].sample(n=pick_n))


if __name__ == '__main__':
    conn = pymssql.connect(host='140.138.155.188', user='sa', password='ltlab1612b', database='finalproject1091')
    cur = conn.cursor()
    cur.execute('SELECT * FROM [dbo].[restaurant];')
    table = cur.fetchall()
    df = DataFrame(table, columns=['key','name','type','address','image','rank'])
    # file_title = 'C:/Users/user/Documents/1091雲端/finalproject/test.xlsx'
    # df.to_excel(file_title, index=False)
    Fliter(df, header='type', text='正餐', pick_n=5)
    cur.close()
    conn.close()