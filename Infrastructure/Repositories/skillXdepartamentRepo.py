from Domain.extension import skillXdepartamentCollection,skillCollection

def postSkillToDepartamentRepo(skill):

    # GENEREZ INTAI ID PENTRU DOCUMENT DUPA APELEZ PENTRU POSTARE IN DATABASE
    insertedItm = skillXdepartamentCollection.document()
    documentId = insertedItm.id

    skill["id"] = documentId

    insertedItm.set(skill)

    return skill

def getSkillsFromDepartmentRepo(departmentId):

    query = skillXdepartamentCollection.where("departamentId", "==", departmentId).get()

    skills = []

    for doc in query:

        skillId = doc.get("skillId")

        doc = skillCollection.document(skillId).get()

        if doc.exists:
            skill_data = doc.to_dict()
            skills.append(skill_data.get("name", ""))

    return skills


