from bson import ObjectId

from Domain.extension import employeesCollection



def postUserRepository(user):

    # GENEREZ INTAI ID PENTRU DOCUMENT DUPA APELEZ PENTRU POSTARE IN DATABASE
    insertedItm = employeesCollection.document()
    documentId = insertedItm.id
    user["id"] = documentId

    insertedItm.set(user)

    return user



def getUserByIdRepository(id):
    return employeesCollection.document(id).get()

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