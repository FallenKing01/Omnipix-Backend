from Domain.extension import endorsmentCollection,assignedSkillCollection,skillXprojectCollection,employeesCollection,customTeamRoleCollection,organizationXadminCollection,projectManagerCollection,departamentManagerCollection
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token
from Utils.Exceptions.customException import CustomException
import time
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

def updateUserDepartamentRepository(user):

    query = employeesCollection.where("id", "==", user["employeeId"]).limit(1).get()

    for doc in query:
        doc.reference.update({"departamentId": user["departamentId"]})

def postCustomRoleRepository(role):

    insertedItm = customTeamRoleCollection.document()
    documentId = insertedItm.id

    role["id"] = documentId

    insertedItm.set(role)

    return role

def getUserRolesRepo(id):
    employeeRoles = {
        "admin": bool(organizationXadminCollection.where("employeeId", "==", id).get()),
        "departmentManager": bool(departamentManagerCollection.where("employeeId", "==", id).get()),
        "projectManager": bool(projectManagerCollection.where("employeeId", "==", id).get()),
    }

    return employeeRoles

def postSkillInProjectRepo(skill):

    insertedItm = skillXprojectCollection.document()
    insertedItmId = insertedItm.id

    skill["id"] = insertedItmId

    skillXprojectCollection.add(skill)

    return skill


def deleteSkillFromProjectRepo(id):

    query = skillXprojectCollection.where("id", "==", id).get()

    for doc in query:

        doc_ref = skillXprojectCollection.document(doc.id)
        doc_ref.delete()


def getSkillsFromProjectRepo(id):

    query = skillXprojectCollection.where("projectId", "==", id).get()

    skills = []

    for doc in query:
        currentDoc = doc.to_dict()
        skills.append(currentDoc)

    return skills

def getOrganizationEmployeesRepo(id):
    query = employeesCollection.where("organizationId", "==", id).get()
    employees = []

    for doc in query:
        currentDoc = doc.to_dict()
        currentDoc.pop("password", None)
        employees.append(currentDoc)

    return employees

def getDepartamentEmployeesRepo(id):
    query = employeesCollection.where("departamentId", "==", id).get()

    employees = []

    for doc in query:

        currentDoc = doc.to_dict()
        currentDoc.pop("password", None)
        employees.append(currentDoc)

    return employees

def getInactiveAssignSkills(departamentId):

    query = employeesCollection.where("departamentId","==",departamentId).get()

    employeeIds = []

    for doc in query:
        currentDoc = doc.to_dict()
        currentDoc.pop("password",None)
        employeeIds.append(currentDoc["id"])

    if not employeeIds:
        raise CustomException(404,"Employees not found")

    query = assignedSkillCollection.where("employeeId","in",employeeIds).where("isApproved","==",None).get()

    skills = []

    for doc in query:
        skills.append(doc.to_dict())

    if not skills:
        raise CustomException(404, "Skills not found")

    return skills

def acceptProposalForSkill(id):

    query = assignedSkillCollection.where("id","==",id).get()

    for doc in query:
        doc.reference.update({"isApproved":True,"dateTime":datetime.utcnow()})

def declineProposalForSkill(id):

    query = assignedSkillCollection.where("id", "==", id).get()

    for doc in query:
        doc.reference.delete()


def getEndorsmentOfSkill(skillId):
    query = endorsmentCollection.where("assignedSkillId","==",skillId).get()

    for doc in query:
        endorsment = doc.to_dict()

    return endorsment