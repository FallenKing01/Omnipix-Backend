from Domain.extension import organizationCollection

def postOrganizationAdminRepository(organizationAdmin):

    # GENEREZ INTAI ID PENTRU DOCUMENT DUPA APELEZ PENTRU POSTARE IN DATABASE
    insertedItm = organizationCollection.document()
    documentId = insertedItm.id

    organizationAdmin["id"] = documentId

    insertedItm.set(organizationAdmin)

    return organizationAdmin