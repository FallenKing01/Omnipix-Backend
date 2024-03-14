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

    insertProject = {}
    insertedItm = projectManagerCollection.document()
    insertedItmId = insertedItm.id
    insertProject["id"] = insertedItmId
    insertProject["employeeId"] = project["employeeId"]
    insertProject["projectId"] = project["projectId"]

    projectManagerCollection.add(insertProject)



def searchForUserRepo(employee):
    query = employeesCollection.where("organizationId", "==", employee["organizationId"]).get()

    searchResult = []

    for doc in query:
        employee_data = doc.to_dict()

        employee_data.pop("password", None)

        input_name_lower = employee["name"].lower()
        employee_name_lower = employee_data["name"].lower()

        if input_name_lower in employee_name_lower:
            searchResult.append(employee_data)

    return searchResult

def DdeleteProjectManagerRepo(employeeId):

    query = projectManagerCollection.where("employeeId","==",employeeId).get()

    for doc in query:
        doc.reference.delete()








