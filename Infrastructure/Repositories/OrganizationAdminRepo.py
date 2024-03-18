from Domain.extension import organizationCollection,organizationXadminCollection,customTeamRoleCollection

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
