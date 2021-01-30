from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SAMPLE_SPREADSHEET_ID = "1FljW9_F-hoLI-yvrwdSdaE7MKC4vN1Lui6oiallGJEM"

service = build('sheets', 'v4', credentials=credentials)

sheet = service.spreadsheets()


def get_sheet_content():
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="2016-2020",
                                valueRenderOption='UNFORMATTED_VALUE', dateTimeRenderOption='SERIAL_NUMBER').execute()
    values = result.get('values', [])
    return values


def get_excel_column_name(n): return '' if n <= 0 else get_excel_column_name(
    (n - 1) // 26) + chr((n - 1) % 26 + ord('A'))


def get_date_column(values):
    for i in range(len(values[1])):
        cell = values[1][i]
        if(str(cell).isnumeric()):
            excel_date = cell
            dt = datetime.fromordinal(
                datetime(1900, 1, 1).toordinal() + excel_date - 2)
            today = datetime.today()
            #today = datetime(2020, 9, 10)
            if(today.date() == dt.date()):
                return get_excel_column_name(i+1)
    return None


def get_id_row(values, id):
    for i in range(len(values)):
        if(values[i][2] == id):
            return i+1
    return None


def write_presence(values, id):
    column = get_date_column(values)
    row = get_id_row(values, id)
    if row is not None and column is not None:
        request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, valueInputOption="USER_ENTERED",
                                        range="2016-2020!"+str(column)+str(row), body={"values": [["X"]]}).execute()


values = get_sheet_content()
write_presence(values, 'testid')
