from pymongo import MongoClient
from bson.objectid import ObjectId

# TODO: change URL and cluster name
cluster = MongoClient(
    "mongodb+srv://attendance:mysvu4-toxnox-Ramdic@attendance.yxtwy.mongodb.net/Attendance?retryWrites=true&w=majority")
db = cluster["Attendance"]
collection = db["Users"]


def post_to_db(firstName,lastName,dob,telephone,email,rank,encoding):
    post = {"firstName": firstName, "lastName": lastName, "dob": dob, "telephone": telephone, "email": email, "rank": rank, "encoding":encoding}
    id = collection.insert_one(post)
    return id.inserted_id


def get_documents():
    documents = collection.find({})
    return documents


