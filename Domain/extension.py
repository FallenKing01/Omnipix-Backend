import bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api
from firebase_admin import credentials, firestore
import firebase_admin


api = Api()
jwt = JWTManager()
#crypt password
salt = bcrypt.gensalt()

authorizations = {
    "jsonWebToken": {"type": "apiKey", "in": "header", "name": "Authorization"}
}
#database setup
cred = credentials.Certificate("team-finder-app-c0d6a-firebase-adminsdk-xalm3-d272e9e0a2.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
#collections
employeesCollection = db.collection('employee')
organizationCollection  = db.collection('organization')



