"""
    File handling the global data required in the whole application.
    This concerns the list of known face encodings, the list of users
    in the database and the list of users in the spreadsheet.
"""

from database import get_documents
from participant_list import get_sheet_content


def init():
    """
        Fetches all the information from the database and the spreadsheet.
    """
    global known_encodings
    global users
    global values

    # Get documents from the database
    docs = get_documents()
    known_encodings = []
    users = []
    for d in docs:
        known_encodings.append(d["encoding"])
        users.append({"_id": str(d["_id"]), "name": d["firstName"],
                      "telehpone": d["telephone"], "email": d["email"]})

    # Get values from the spreadsheet
    values = get_sheet_content()


def update_db():
    """
        Fetch the database documents and update the corresponding global
        variables.
    """
    global known_encodings
    global users
    docs = get_documents()
    known_encodings = []
    users = []
    for d in docs:
        known_encodings.append(d["encoding"])
        users.append({"_id": str(d["_id"]), "name": d["firstName"],
                      "telehpone": d["telephone"], "email": d["email"]})


def update_spreadsheet():
    """
        Fetch the spreadsheet values and update the corresponding global
        variable.
    """
    global values
    values = get_sheet_content()
