from Domain.extension import organizationXadminCollection

def postorganizationXadminRepository(organizationxadmin):

    # GENEREZ INTAI ID PENTRU DOCUMENT DUPA APELEZ PENTRU POSTARE IN DATABASE
    insertedItmId = organizationXadminCollection.document()
    documentId = insertedItmId.id

    organizationxadmin["id"] = documentId

    insertedItmId.set(organizationxadmin)

    return organizationxadmin