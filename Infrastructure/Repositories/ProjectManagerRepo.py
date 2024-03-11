from Domain.extension import projectManagerCollection,employeesCollection
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


def searchForUserRepo(employee):
    query = employeesCollection.where("organizationId", "==", employee["organizationId"]).get()

    searchResult = []

    for doc in query:
        employee_data = doc.to_dict()

        # Remove the 'password' field if it exists
        employee_data.pop("password", None)

        # Convert both input name and employee name to lowercase for case-insensitive comparison
        input_name_lower = employee["name"].lower()
        employee_name_lower = employee_data["name"].lower()

        # Check if the input name is contained within the employee name (case-insensitive)
        if input_name_lower in employee_name_lower:
            # Include the document data in the search result
            searchResult.append(employee_data)

    return searchResult








