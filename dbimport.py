import boto3
import pymssql
from pandas import DataFrame

conn = pymssql.connect(host='140.138.155.188', user='sa', password='ltlab1612b', database='finalproject1091')
cur = conn.cursor()
cur.execute('SELECT * FROM [dbo].[restaurant];')
table = cur.fetchall()
restaurantDF = DataFrame(table, columns=['resID','name','type','address','image','rank'])
cur.close()
conn.close()

def importData(dynamodb=None):
    dynamodb = boto3.resource('dynamodb', region_name="us-east-1", aws_access_key_id='ASIASAILT6CMOBR73QMT', aws_secret_access_key='VwNbhhVFa7dIIGYEi2fKxqoWcpPZ84LAfO9uAyRW', aws_session_token='FwoGZXIvYXdzELj//////////wEaDLdygQFxEAXH8gBqpyLIATFYel5EVpgUJdVOSfHjWCy8g0ybaEQ2Qq9cl318HtHEOdAXWdgs2otk+m9uE5NGEfd9f4lQ+pRiV+D4UCi0rnC1kS1WDYhd3O6UkLlOFUTY7V8PTv1QsUPLhnGYMH8uDHt27hs3/Tn9aRPYHFI/3ERtR3+hPRuYXCLp/KBG/iWmxWiqDhD/003rFZsqEJVl+FcPhPSdePm7UkFX1WwPMKCqqOHrs8Pjx0t10SCLjdWgbUk1ZcXJSah+60fNw203OV+MWQipBkdUKO2Y5f8FMi1O9FUMb/Kj7R4v1A5NNqmPAu7KMbRyDShHjoZjEdLF51p080I1bIircfv5vlU=')
    table = dynamodb.Table('linebot_EATWhat_DB')
    # 寫入
    
    print(table.item_count)
    #計算表單上的數量是否與DB相同，較多則新增
    for i in range(len(restaurantDF)-table.item_count):
        # 批次寫入
        index = i+table.item_count
        table.put_item(
            Item={
                'resID': str(restaurantDF.iloc[index]['resID']),
                'resName': restaurantDF.iloc[index]['name'],
                'resType': restaurantDF.iloc[index]['type'],
                'resAddress': restaurantDF.iloc[index]['address'],
                'resImage': restaurantDF.iloc[index]['image'],
                'resRank': restaurantDF.iloc[index]['rank']
            }
        )

    return None
 
if __name__ == '__main__':
    
   importData()
    