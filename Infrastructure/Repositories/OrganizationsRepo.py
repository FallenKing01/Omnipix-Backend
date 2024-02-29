from Domain.extension import organizationCollection


def postOrganizationRepository(organization):

    # GENEREZ INTAI ID PENTRU DOCUMENT DUPA APELEZ PENTRU POSTARE IN DATABASE
    insertedItm = organizationCollection.document()
    documentId = insertedItm.id

    organization["id"] = documentId

    insertedItm.set(organization)

    return organization