from database import get_documents
from participant_list import get_sheet_content


def init():
    global known_encodings
    global users
    global values
    docs = get_documents()
    known_encodings = []
    users = []
    for d in docs:
        known_encodings.append(d["encoding"])
        users.append({"_id":str(d["_id"]),"name":d["firstName"],"telehpone":d["telephone"],"email":d["email"]})

    values = get_sheet_content()
    
def update_db():
    global known_encodings
    global users
    docs = get_documents()
    known_encodings = []
    users = []
    for d in docs:
        known_encodings.append(d["encoding"])
        users.append({"_id":str(d["_id"]),"name":d["firstName"],"telehpone":d["telephone"],"email":d["email"]})
        
def update_spreadsheet():
    global values
    values = get_sheet_content()