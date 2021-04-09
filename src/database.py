"""
    Handles the communication with the MongoDB database
"""

from pymongo import MongoClient
from bson.objectid import ObjectId
import info

cluster = MongoClient(
    "mongodb+srv://attendance:mysvu4-toxnox-Ramdic@attendance.yxtwy.mongodb.net/Attendance?retryWrites=true&w=majority")
db = cluster["Attendance"]
collection = db["Users"]


def post_to_db(first_name, last_name, dob, telephone, email, rank, encoding):
    """
        Add a user to the database.

        :param first_name: first name of the user
        :param last_name: last name of the user
        :param dob: date of birth of the user
        :param telephone: telephone number of the user
        :param email: emain address of the user
        :param rank: belt rank of the user
        :param encoding: face encoding of the user

        :return: id of the newly insterted user
    """
    post = {"firstName": first_name, "lastName": last_name, "dob": dob,
            "telephone": telephone, "email": email, "rank": rank, "encoding": encoding}
    id = collection.insert_one(post)
    info.update_db()
    return id.inserted_id


def get_documents():
    """
        Fetch all users from the database
    """
    documents = collection.find({})
    return documents
