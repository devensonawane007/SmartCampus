import os
import firebase_admin
from firebase_admin import credentials, db

# Path to the service account JSON (next to run.py)
cred_path = os.path.join(os.path.dirname(__file__), '../firebase_key.json')
cred = credentials.Certificate(cred_path)

# Initialize Firebase Admin SDK
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smartcampus-bbd3f-default-rtdb.firebaseio.com'
})

# Reference to root of database
db_ref = db.reference('/')

# Optional: make this available for imports
firebase = firebase_admin
