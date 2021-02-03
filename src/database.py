from pymongo import MongoClient
from bson.objectid import ObjectId

# TODO: change URL and cluster name
cluster = MongoClient(
    "mongodb+srv://miromatagne:Mmm2000(@proj-h-402.zpee0.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = cluster["Test"]
collection = db["Users"]


def post_to_db():
    post = {"name": "Miro", "age": 20, "encodings": [[1, 2, 3], [4, 5, 6]]}

    collection.insert_one(post)


# def add_image():
#     collection.update_one({"_id": ObjectId("5fc61ba448f61a6793b485cf")}, {'$push': {
#         'photos': "https://media.resources.festicket.com/www/artists/KendrickLamar_New.jpg"}})


def get_documents():
    documents = collection.find({})
    users = {}
    for doc in documents:
        user = {"name": doc["name"], "age": doc["age"]}
        encoding = doc["encoding"]
        users[str(doc["_id"])] = {"user": user, "encoding": encoding}
    return users


post_to_db()
