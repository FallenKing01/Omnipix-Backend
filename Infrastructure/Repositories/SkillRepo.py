from Domain.extension import skillCollection,assignedSkillCollection
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

    query = assignedSkillCollection.where("employeeId", "==", employeeId).stream()

    skills = []
    for doc in query:

        data = doc.to_dict()

        skillId = data.get("skillId", "")

        skillDoc = skillCollection.document(skillId).get()

        if skillDoc.exists:
            skill = {}

            skill_name = skillDoc.get("name")
            skill["name"] = skill_name if skill_name is not None else ""
            skill["level"] = data["level"]
            skill["experience"] = data["experience"]
            skills.append(skill)

    return skills

