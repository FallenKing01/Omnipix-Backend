from Domain.extension import skillXdepartamentCollection,skillCollection
from Utils.Exceptions.customException import CustomException
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
    result = []
    if query:
        for doc in query:
            currentDoc = doc.to_dict()

            skill_doc = skillCollection.document(currentDoc["skillId"]).get()

            if skill_doc.exists:
                skill_data = skill_doc.to_dict()

                currentDoc["skillId"] = skill_data
                result.append(skill_data)
                skills.append(currentDoc)

    return result


def getAvailableDepartamentSkills(departamentId,organizationId):
    query = skillXdepartamentCollection.where("departamentId", "==", departamentId).get()
    print(query)
    skillsOwned = []
    if not query:
        skilLsQuery = skillCollection.where("organizationId", "==", organizationId).get()
        for doc in skilLsQuery:
            skillsOwned.append(doc.to_dict())
        return skillsOwned

    if query:
        for doc in query:
            curentDoc = doc.to_dict()
            skillsOwned.append(curentDoc["skillId"])
    else:
        raise CustomException(404, "No skills available for this departament")

    querySkills = skillCollection.where("organizationId", "==", organizationId).get()

    if not querySkills:
        raise CustomException(404, "No skills available for this departament")

    availableSkills = []

    for doc in querySkills:
        doc_dict = doc.to_dict()
        if doc_dict["id"] not in skillsOwned:
            availableSkills.append(doc_dict)

    return availableSkills


