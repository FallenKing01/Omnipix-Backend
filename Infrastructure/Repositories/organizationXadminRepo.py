from Domain.extension import organizationXadmin

def postorganizationXadminRepository(organizationxadmin):

    # GENEREZ INTAI ID PENTRU DOCUMENT DUPA APELEZ PENTRU POSTARE IN DATABASE
    insertedItmId = organizationXadmin.document()
    documentId = insertedItmId.id

    organizationxadmin["id"] = documentId

    insertedItmId.set(organizationxadmin)

    return organizationxadmin