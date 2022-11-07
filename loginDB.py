import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def setUpDatabase():
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

    db=firestore.client()
    db.collection('users').add({'username': 'testuser'})



