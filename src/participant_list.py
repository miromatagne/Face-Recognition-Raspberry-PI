"""
    Handles all interactions with the Google Sheets spreadsheet.
"""

from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
import info

# Global variables allowing to identify the spreadsheet
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = '../keys.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SAMPLE_SPREADSHEET_ID = "1FljW9_F-hoLI-yvrwdSdaE7MKC4vN1Lui6oiallGJEM"

service = build('sheets', 'v4', credentials=credentials)

# Build the sheet object
sheet = service.spreadsheets()


def get_sheet_content():
    """
        Fetches all the information contained in the spreadsheet.

        :return values: all values contained in the spreadsheet
    """
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="2016-2020",
                                valueRenderOption='UNFORMATTED_VALUE', dateTimeRenderOption='SERIAL_NUMBER').execute()
    values = result.get('values', [])
    return values


def get_excel_column_name(n):
    """
        Computes the Excel colum name from an index

        :param n: index of the column

        :return: column name (or empty string if error)
    """
    return '' if n <= 0 else get_excel_column_name((n - 1) // 26) + chr((n - 1) % 26 + ord('A'))


def get_date_column(values):
    """
        Finds the column corresponding the the actual date.

        :param values: all the values of the spreadsheet

        :return: the column index
    """
    for i in range(len(values[1])):
        cell = values[1][i]
        if(str(cell).isnumeric()):
            excel_date = cell
            dt = datetime.fromordinal(
                datetime(1900, 1, 1).toordinal() + excel_date - 2)
            today = datetime.today()
            #today = datetime(2020, 9, 16)
            if(today.date() == dt.date()):
                return get_excel_column_name(i+1)
    return write_new_column(values)


def get_id_row(values, id):
    """
        Gets the index of a row corresponding to a certain user Id

        :param values: values contained in the spreadsheet
        :param id: id of the user

        :return: row index (or None if user id was not found in the spreadsheet)
    """
    for i in range(len(values)):
        if(values[i][2] == id):
            return i+1
    return None


def get_name_row(values, first_name, last_name):
    """
        Find a row of the spreadsheet based on a user's first and last name

        :param values: all the values of the spreadsheet
        :param first_name: first name of the user
        :param last_name: last name of the user

        :return: row index corresponding to that user
    """
    for i in range(len(values)):
        if(values[i][0] == first_name and values[i][1] == last_name):
            return i+1
    return None


def write_presence(values, id):
    """
        Marks the presence of a certain user by an X in the row corresponding to
        the user and the column corresponding to the date, knowing the user's id.

        :param values: all values of the spreadsheet
        :param id: id of the user to be marked as present
    """
    # Get row and column where the X should be written
    column = get_date_column(values)
    row = get_id_row(values, id)
    if row is not None and column is not None:
        request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, valueInputOption="USER_ENTERED",
                                        range="2016-2020!"+str(column)+str(row), body={"values": [["X"]]}).execute()


def write_presence_from_name(values, first_name, last_name):
    """
        Marks the presence of a certain user by an X in the row corresponding to
        the user and the column corresponding to the date, knowing the user's first
        and last names.

        :param values: all values of the spreadsheet
        :param first_name: first name of the user to be marked as present
        :param last_name: last name of the user to be marked as present
    """
    # Get row and column where the X should be written
    column = get_date_column(values)
    row = get_name_row(values, first_name, last_name)
    if row is not None and column is not None:
        request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, valueInputOption="USER_ENTERED",
                                        range="2016-2020!"+str(column)+str(row), body={"values": [["X"]]}).execute()


def add_user(first_name, last_name, dob, telephone, email, rank, id):
    """
        Add a new user to the spreadsheet.

        :param first_name: first name of the user
        :param last_name: last name of the user
        :param dob: date of birth of the user
        :param telephone: telephone number of the user
        :param email: email address of the user
        :param rank: belt rank of the user
        :param id: id of the user
    """
    request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, valueInputOption="USER_ENTERED",
                                    range="2016-2020", body={"values": [[first_name, last_name, str(id), '', telephone, email, dob, '', '', rank]]}).execute()
    info.update_spreadsheet()


def write_new_column(values):
    """
        Write a new column to the spreadsheet. This is useful when
        the actual date is not present in the spreadsheet.

        :param values: all values of the spreadsheet

        :return: index of the newly created column
    """
    nbRow = 2
    maxList = max(values, key=lambda i: len(i))
    nbCol = get_excel_column_name(len(maxList) + 1)
    today = datetime.today()
    date = today.strftime("%m/%d/%Y")
    body = {
        "requests": [
            {
                "appendDimension": {
                    "sheetId": 1849052962,
                    "dimension": "COLUMNS",
                    "length": 1
                }
            }
        ]
    }
    request = service.spreadsheets().batchUpdate(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, body=body).execute()
    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, valueInputOption="USER_ENTERED",
                                    range="2016-2020!"+str(nbCol)+str(nbRow), body={"values": [[date]]}).execute()
    info.update_spreadsheet()
    return nbCol


def write_new_id(values, index, new_id):
    """
        Write a new id to a user in the spreadsheet. This is used when an
        already existing member registers to the database, and therefore 
        recevives an id.

        :param values: all values of the spreadsheet
        :param index: index of the user that needs an id
        :param new_id: id to be given to this user
    """
    nbCol = "C"
    nbRow = index+1
    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, valueInputOption="USER_ENTERED",
                                    range="2016-2020!"+str(nbCol)+str(nbRow), body={"values": [[str(new_id)]]}).execute()
    info.update_spreadsheet()
