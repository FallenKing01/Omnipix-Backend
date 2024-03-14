from Domain.extension import organizationCollection,organizationXadminCollection

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