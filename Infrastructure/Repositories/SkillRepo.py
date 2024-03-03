from Domain.extension import skillCollection


def postSkillRepo(skill):

    # GENEREZ INTAI ID PENTRU DOCUMENT DUPA APELEZ PENTRU POSTARE IN DATABASE
    insertedItm = skillCollection.document()
    documentId = insertedItm.id

    skill["id"] = documentId

    insertedItm.set(skill)

    return skill

def getOrganizationSkillsRepo(id):
    skills = []

    organizationSkills = skillCollection.where('organizationId', '==', id).stream()

    for currentSkill in organizationSkills:
        skills.append(currentSkill.to_dict())

    return skills