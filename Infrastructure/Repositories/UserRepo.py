from Domain.extension import (skillCollection,endorsmentCollection,assignedSkillCollection,
                              skillXprojectCollection,employeesCollection,customTeamRoleCollection,
                              organizationXadminCollection,projectManagerCollection,departamentManagerCollection,salt)
import bcrypt
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token
from Utils.Exceptions.customException import CustomException

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

    user["departamentId"]=None
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
    # Hash the new password with bcrypt
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

    # Update the password in the database
    query = employeesCollection.where("email", "==", email).limit(1).get()

    for doc in query:
        doc.reference.update({"password": hashed_password.decode('utf-8')})


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

        currentDoc = doc.to_dict()
        skillQuery = skillCollection.where("id","==",currentDoc["skillId"]).get()
        if skillQuery:
            for skillDoc in skillQuery:
                currentDoc["skillData"] = skillDoc.to_dict()

        queryEmployee = employeesCollection.where("id","==",currentDoc["employeeId"]).get()

        if queryEmployee:
            for employeeDoc in queryEmployee:
                currentEmployee = employeeDoc.to_dict()
                currentEmployee.pop("password",None)
                currentDoc["employeeData"] = currentEmployee

        skills.append(currentDoc)


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

def getInfoAboutUserRepo(id):
    query = employeesCollection.where("id", "==", id).limit(1).get()

    userInfo = {}

    for doc in query:
        user_data = doc.to_dict()

        for key, value in user_data.items():
            if isinstance(value, bytes):
                user_data[key] = value.decode('utf-8')

        userInfo = user_data

    return userInfo

def getEmployeesNoDepartament(organizationId):
    query = employeesCollection.where("organizationId","==",organizationId).where("departamentId","==",None).get()

    employees = []

    for doc in query:
        currentDoc = doc.to_dict()
        currentDoc.pop("password",None)
        employees.append(currentDoc)

    return employees

def updateEmployeeEmailNameRepo(employeeId, email, name):
    query = employeesCollection.where("id", "==", employeeId).limit(1).get()

    queryEmployee = employeesCollection.where("email", "==", email).limit(1).get()

    for doc in queryEmployee:
        currentDoc = doc.to_dict()
        emailDb = currentDoc["email"]


    if emailDb == email:
        doc.reference.update({"name": name})
    else:
        queryEmployee = employeesCollection.where("email", "==", email).limit(1).get()
        if queryEmployee:
            raise CustomException(409,"Email is already used")

        doc.reference.update({"email":email,"name": name})


def getNotAssignedSkillsOfEmployeeRepo(employeeId,organizationId):

    query = assignedSkillCollection.where("employeeId","==",employeeId).get()

    assignedSkills = []

    if not query:
        query = skillCollection.where("organizationId", "==", organizationId).get()

        if not query:
            raise CustomException(404, "Skills not found")

        skills = []
        for doc in query:
            currentDoc = doc.to_dict()
            skills.append(currentDoc)

        return skills

    for doc in query:
        currentDoc = doc.to_dict()
        assignedSkills.append(currentDoc["skillId"])

    query = skillCollection.where("organizationId","==",organizationId).get()
    for doc in query:
        currentDoc = doc.to_dict()
        if currentDoc["id"] in assignedSkills:
            query.remove(doc)

    skills = []

    for doc in query:
        currentDoc = doc.to_dict()
        skills.append(currentDoc)

    return skills

def ableToAssignSkillRepo(employeeId):

    query = employeesCollection.where("id","==",employeeId).get()

    for doc in query:
        currentDoc = doc.to_dict()
        if currentDoc["departamentId"] is None:
            return False
    return True