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


def updateProjectsOfManager(project):
    documents = projectManagerCollection.where("employeeId", "==", project["employeeId"]).get()

    print(documents)

    for document in documents:
        projectIds = document.get("projectId")

        if projectIds is None:
            projectIds = []

        projectIds.append(project["projectId"])
        print(projectIds)

        document.reference.update({"projectId": projectIds})