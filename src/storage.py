from google.cloud import storage
import time

BUCKET_NAME = 'verylonguniquebucketname'


def store_picuture(im, user):
    # TODO add key.json to repository once account is created
    storage_client = storage.Client.from_service_account_json(
        'key.json')
    bucket = storage_client.get_bucket(BUCKET_NAME)
    millis = str(round(time.time() * 1000))
    blob = bucket.blob(user.name + "/" + millis)
    blob.upload_from_file(im)

