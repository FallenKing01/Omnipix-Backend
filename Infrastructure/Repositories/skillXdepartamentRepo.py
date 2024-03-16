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

    if query:
        for doc in query:
            skills.append(doc.to_dict())

    return skills


