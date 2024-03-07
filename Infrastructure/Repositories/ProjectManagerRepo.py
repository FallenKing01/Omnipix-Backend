from Domain.extension import projectManagerCollection
def postProjectManagerRepo(id):

    insertedProjectManager = {
        "employeeId":id,
        "projectId":None,
    }

    insertedItmInDoc = projectManagerCollection.document()
    documentId = insertedItmInDoc.id

    insertedProjectManager["id"] = documentId

    insertedItmInDoc.set(insertedProjectManager)

    return insertedProjectManager

