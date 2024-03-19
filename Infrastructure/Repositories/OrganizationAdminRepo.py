from Domain.extension import organizationCollection,organizationXadminCollection,customTeamRoleCollection,projectXemployeeCollection

def postOrganizationAdminRepository(organizationAdmin):

    # GENEREZ INTAI ID PENTRU DOCUMENT DUPA APELEZ PENTRU POSTARE IN DATABASE
    insertedItm = organizationCollection.document()
    documentId = insertedItm.id

    organizationAdmin["id"] = documentId

    insertedItm.set(organizationAdmin)

    return organizationAdmin

def createNewOrganizationAdminRepo(employeeId,organizationId):

    insertedItm = organizationXadminCollection.document()
    insertedItmId = insertedItm.id

    newAdmin = {
        "id":insertedItmId,
        "employeeId":employeeId,
        "organizationId":organizationId,
    }

    organizationXadminCollection.add(newAdmin)

def deleteOrganizationAdminRoleRepo(employeeId):

    query = organizationXadminCollection.where("employeeId","==",employeeId).get()

    for doc in query:
        doc.reference.delete()

def updateCustomRoleRepo(customRoleId,newRoleName):

    query = customTeamRoleCollection.where("id","==",customRoleId).get()

    for doc in query:
        doc.reference.update({"name":newRoleName})

def getCustomRoleFromOrganizationRepo(organizationId):

    query = customTeamRoleCollection.where("organizationId","==",organizationId).get()

    teamRoles = []

    if query:
        for doc in query:
            currentDoc = doc.to_dict()
            teamRoles.append(currentDoc)

    return teamRoles

def deleteCustomTeamRoleRepo(customRoleId, organizationId):

    query = customTeamRoleCollection.where("id", "==", customRoleId).get()
    for doc in query:
        doc.reference.delete()

    query = projectXemployeeCollection.where("organizationId", "==", organizationId).get()
    for doc in query:
        roles = []
        currentDoc = doc.to_dict()
        employeeRoles = currentDoc["employeeRolesId"]
        for value in employeeRoles:
            if value != customRoleId:
                roles.append(value)
        doc.reference.update({"employeeRolesId": roles})



