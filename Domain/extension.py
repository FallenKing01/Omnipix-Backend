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
organizationXadminCollection = db.collection('organizationXadmin')
departamentCollection = db.collection("departament")
departamentManagerCollection = db.collection('departamentManager')
skillCollection = db.collection('skill')
assignedSkillCollection = db.collection("assignedSkill")
endorsmentCollection = db.collection("endorsment")
customTeamRoleCollection = db.collection("teamRole")
skillXdepartamentCollection = db.collection("skillXdepartament")
projectManagerCollection = db.collection("projectManager")
technologyStackCollection = db.collection("technologyStack")
projectCollection = db.collection("project")
projectStatusCollection = db.collection("projectStatus")
skillXprojectCollection = db.collection("skillXproject")
assignementProposalCollection = db.collection("assginmentProposal")
dealocationProposalCollection = db.collection("dealocationProposal")