import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage

def setUpDatabase():
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

    db=firestore.client()
    db.collection('users').add({'username': 'testuser'})

def save_photo_to_firebase_storage():
    filePath = 'person.jpg'
    bucket = storage.bucket()
    blob = bucket.blob(filePath)
    blob.upload_from_filename(filePath)




