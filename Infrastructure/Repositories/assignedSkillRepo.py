from Domain.extension import assignedSkillCollection,endorsmentCollection
def postSkillWithEndorsmentRepo(skillAssigned,endorsementsAssigned):

    insertedItm = assignedSkillCollection.document()
    documentId = insertedItm.id

    skillAssigned["isApproved"] = None
    skillAssigned["id"] = documentId
    skillAssigned["dateTime"] = None
    skillAssigned.pop("endorsements")
    insertedItm.set(skillAssigned)
    insertedEndorsements = []

    if not endorsementsAssigned:

        return skillAssigned, insertedEndorsements

    else:

        for endorsement in endorsementsAssigned:
            insertedEndorsement = endorsmentCollection.document()
            endorsementDocumentId = insertedEndorsement.id

            endorsement["id"] = endorsementDocumentId
            endorsement["assignedSkillId"] = skillAssigned["id"]

            insertedEndorsement.set(endorsement)
            insertedEndorsements.append(endorsement)

    return skillAssigned, insertedEndorsements
