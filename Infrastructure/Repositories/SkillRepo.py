from Domain.extension import skillCollection,assignedSkillCollection
from Utils.Exceptions.customException import CustomException
def postSkillRepo(skill):

    # GENEREZ INTAI ID PENTRU DOCUMENT DUPA APELEZ PENTRU POSTARE IN DATABASE
    insertedItm = skillCollection.document()
    documentId = insertedItm.id

    skill["currentManager"] = skill["authorId"]
    skill["id"] = documentId

    insertedItm.set(skill)

    return skill

def getOrganizationSkillsRepo(id):

    skills = []

    organizationSkills = skillCollection.where('organizationId', '==', id).stream()

    for currentSkill in organizationSkills:
        skills.append(currentSkill.to_dict())

    return skills


def getSkillByIdRepo(id):

    query = skillCollection.where('id', '==', id).stream()

    skill = None

    for doc in query:
        skill = doc.to_dict()
        break

    return skill

def getSkillByAutorIdRepo(id):
    query = skillCollection.where('authorId', '==', id).get()

    skills = []

    for doc in query:
        # Append each document to the skills list
        skills.append(doc.to_dict())

    return skills



def getSkillsOfEmployeeRepo(employeeId):

    query = assignedSkillCollection.where("employeeId", "==", employeeId).get()

    skills = []
    for doc in query:

        data = doc.to_dict()

        skillId = data.get("skillId", "")

        skillDoc = skillCollection.document(skillId).get()

        if skillDoc.exists:
            skillDoc = skillDoc.to_dict()
            skillDoc["isApproved"] = data["isApproved"]
            skillDoc["assignedSkillId"] = data["id"]
            skills.append(skillDoc)

    return skills

def updateSkillRepo(skill):

    query = skillCollection.where("id","==",skill["skillId"]).limit(1).get()

    for doc in query:
        if doc.get("currentManager") != skill["managerId"]:
            raise CustomException(409,"You can t edit becouse is not your skill")

        skill = doc.reference.update({"description":skill["description"],"category":skill["category"],"name":skill["name"]})
        skill = doc.to_dict()

    return skill


def deleteSkillRepo(id):

    pass
