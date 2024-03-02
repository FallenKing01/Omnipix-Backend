
from Domain.extension import employeesCollection
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token

def signUpToken(user):

    userData = {
        "id": user["id"],
        "name": user["name"],
        "workingHours": user["workingHours"],
        "email": user["email"],
        "organizationId": user["organizationId"],
        "departamentId": user["departamentId"]
    }

    expires = datetime.utcnow() + timedelta(days=30)

    token = create_access_token(
            userData,
            additional_claims=userData,
            expires_delta=expires - datetime.utcnow(),
        )

    return token

def postUserRepository(user):

    # GENEREZ INTAI ID PENTRU DOCUMENT DUPA APELEZ PENTRU POSTARE IN DATABASE
    insertedItm = employeesCollection.document()
    documentId = insertedItm.id

    user["departamentId"]="null"
    user["workingHours"]=0
    user["id"] = documentId

    insertedItm.set(user)

    token = signUpToken(user)

    return token,documentId


def getUserByIdRepository(id):

    query = employeesCollection.where("id", "==", id).limit(1).get()

    user = None
    for doc in query:
        user = doc.to_dict()
        break

    return user


def getUserByEmailRepository(email):
    query = employeesCollection.where("email", "==", email).limit(1).get()
    user = None
    for doc in query:
        user = doc.to_dict()
        break

    return user

def deleteUserByEmailRepository(email):
    query = employeesCollection.where("email", "==", email).limit(1).get()

    for doc in query:
        doc.reference.delete()

def updatePasswordRepository(email, new_password):
    query = employeesCollection.where("email", "==", email).limit(1).get()

    for doc in query:
        doc.reference.update({"password": new_password})