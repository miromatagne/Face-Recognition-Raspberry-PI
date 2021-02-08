from pymongo import MongoClient
from bson.objectid import ObjectId

# TODO: change URL and cluster name
cluster = MongoClient(
    "mongodb+srv://miromatagne:Mmm2000(@proj-h-402.zpee0.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = cluster["proj-h-402"]
collection = db["Users"]


def post_to_db(name,telephone,email,encoding):
    post = {"name": name, "telephone": telephone, "email": email, "encoding":encoding}
    collection.insert_one(post)


def add_image():
    collection.update_one({"_id": ObjectId("5fc61ba448f61a6793b485cf")}, {'$push': {
        'photos': "https://media.resources.festicket.com/www/artists/KendrickLamar_New.jpg"}})


def get_documents():
    documents = collection.find({})
    return documents


