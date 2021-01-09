import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def get_gs():
    scopes = ["https://spreadsheets.google.com/feeds"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scopes)  #  api金鑰

    client = gspread.authorize(credentials)

    sheet = client.open_by_key(
    "1N2o1J_6DPaDVMI_io1jsKu2jWBqOdNL1d8M86xAkBNQ").sheet1  #  google表單的金鑰
    records_data = sheet.get_all_records()
    records_df = pd.DataFrame.from_dict(records_data)

    return records_df  #  return dataframe