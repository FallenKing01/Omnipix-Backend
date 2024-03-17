from Domain.extension import projectManagerCollection,employeesCollection,skillCategoryCollection,technologyStackCollection
from Utils.Exceptions.customException import CustomException
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

def deleteProjectManagerRepo(employeeId):

    query = projectManagerCollection.where("employeeId","==",employeeId).get()

    for doc in query:
        doc.reference.delete()

def postCategory(category):

    insertedItm = skillCategoryCollection.document()
    insertedItmId = insertedItm.id
    category["id"] = insertedItmId

    skillCategoryCollection.add(category)

    return category

def getSkillCategoriesRepo(organizationId):
    query = skillCategoryCollection.where("organizationId", "==", organizationId).get()

    categories = []

    for doc in query:
        category = doc.to_dict()
        categories.append(category)
    if not categories:
        raise CustomException(404, "No categories found")

    return categories

def deleteCategoryRepo(categoryId):
    query = skillCategoryCollection.where("id","==",categoryId).get()

    if not query:
        raise CustomException(404, "Category not found")

    for doc in query:
        doc.reference.delete()

def getTechnologyStackRepo(organizationId):
    query = technologyStackCollection.where("organizationId", "==", organizationId).get()

    technologys = []

    for doc in query:
        category = doc.to_dict()
        technologys.append(category)
    if not technologys:
        raise CustomException(404, "No categories found")

    return technologys

