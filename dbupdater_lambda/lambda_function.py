import boto3
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials


def get_gs():
    scopes = ["https://spreadsheets.google.com/feeds"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scopes)  #  api金鑰

    client = gspread.authorize(credentials)

    sheet = client.open_by_key("1N2o1J_6DPaDVMI_io1jsKu2jWBqOdNL1d8M86xAkBNQ").sheet1  #  google表單的金鑰
    res_data = sheet.get_all_records()
    # records_df = pd.DataFrame.from_dict(records_data)
    return res_data


def importData(rdf, dynamodb=None):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('linebot_EATWhat_DB')
    # 寫入
    
    print(table.item_count)
    #計算表單上的數量是否與DB相同，較多則新增
    for i in range(len(rdf)-table.item_count):
        # 批次寫入
        index = i+table.item_count
        table.put_item(
            Item={
                'resID': str(rdf[index]['resID']),
                'resName': rdf[index]['name'],
                'resType': rdf[index]['type'],
                'resAddress': rdf[index]['address'],
                'resImage': rdf[index]['image'],
                'resRank': rdf[index]['rank']
            }
        )
    return None
 
def lambda_handler(event, context):
    # TODO implement
    importData(get_gs())
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

