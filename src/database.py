from pymongo import MongoClient
from bson.objectid import ObjectId

# TODO: change URL and cluster name
cluster = MongoClient(
    "mongodb+srv://miromatagne:Mmm2000(@proj-h-402.zpee0.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = cluster["proj-h-402"]
collection = db["Users"]


def post_to_db():
    post = {"name": "Miro", "age": 20,
            "photo": "https://storage.cloud.google.com/verylonguniquebucketname/Images/Miro1.JPG"}

    collection.insert_one(post)


def add_image():
    collection.update_one({"_id": ObjectId("5fc61ba448f61a6793b485cf")}, {'$push': {
        'photos': "https://media.resources.festicket.com/www/artists/KendrickLamar_New.jpg"}})


def get_documents():
    documents = collection.find({})
    user_pictures = {}
    for doc in documents:
        user_pictures[doc["_id"]]


add_image()
