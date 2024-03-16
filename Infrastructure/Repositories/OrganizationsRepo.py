from Domain.extension import organizationCollection,customTeamRoleCollection
from Utils.Exceptions.customException import CustomException

def postOrganizationRepository(organization):

    # GENEREZ INTAI ID PENTRU DOCUMENT DUPA APELEZ PENTRU POSTARE IN DATABASE
    insertedItm = organizationCollection.document()
    documentId = insertedItm.id

    organization["id"] = documentId

    insertedItm.set(organization)

    return organization

def getOrganizationByIdRepository(organizationId):

    query = organizationCollection.where("id", "==", organizationId).limit(1).get()

    organization = None

    for doc in query:
        organization = doc.to_dict()
        break

    return organization

def getOrganizationRolesRepo(organizationId):
    query = customTeamRoleCollection.where("organizationId", "==", organizationId).get()

    teamRoles = []

    for doc in query:
        currentDoc = doc.to_dict()
        teamRoles.append(currentDoc)

    if not teamRoles:
        raise CustomException(404,"Team roles not found")

    return teamRoles
