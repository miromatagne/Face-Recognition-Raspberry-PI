from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SAMPLE_SPREADSHEET_ID = "1zFv7RjGGWSI0OXwnRvEqV6_X-zC6kMDwdH3B-2-8oRI"

service = build('sheets', 'v4', credentials=credentials)

sheet = service.spreadsheets()

result = sheet.values().get(
    spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Feuille 1!A1:D5").execute()

# List of lists of all the data we need.
values = result.get('values', [])
print(values)

request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, valueInputOption="USER_ENTERED",
                                range="Feuille 1!D3", body={"values": [["x"]]}).execute()
