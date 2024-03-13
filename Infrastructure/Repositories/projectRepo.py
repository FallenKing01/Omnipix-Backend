from Domain.extension import projectCollection,assignementProposalCollection,projectStatusCollection,employeesCollection,projectXemployeeCollection
from Infrastructure.Repositories.ProjectManagerRepo import updateProjectsOfManager
from datetime import datetime
from Utils.Exceptions.customException import CustomException
def postProjectRepo(project):

    insertedItm = projectCollection.document()
    insertedItmId = insertedItm.id

    updateProjects = {
        "employeeId":project["employeeId"],
        "projectId":insertedItmId
    }

    projectStatus = {
        "projectId": insertedItmId,
        "status":project["status"],
        "creationDate": datetime.utcnow()
    }

    project.pop("status")
    updateProjectsOfManager(updateProjects)

    project["id"] = insertedItmId

    projectStatusCollection.add(projectStatus)
    projectCollection.add(project)

    return project

def updateProjectRepo(project):

    query = projectCollection.where("id", "==", project["projectId"])
    docs = query.get()

    technologyToDelete = project.get("technologyToDelete", [])
    technologyToAdd = project.get("technologyToAdd", [])
    teamRolesToAdd = project.get("teamRolesToAdd", [])
    teamRolesToDelete = project.get("teamRolesToDelete", [])

    for doc in docs:
        doc.reference.update({
            "status": project["status"],
            "name": project["name"],
            "period": project["period"],
            "startDate": project["startDate"],
            "description": project["description"],
        })

        current_technology_stack = doc.to_dict().get("technologyStack", [])

        for tech in technologyToDelete:
            if tech in current_technology_stack:
                current_technology_stack.remove(tech)

        for tech in technologyToAdd:
            current_technology_stack.append(tech)

        doc.reference.update({
            "technologyStack": current_technology_stack
        })

        current_team_roles = doc.to_dict().get("teamRoles", {})

        for role_id in teamRolesToDelete:
            if role_id in current_team_roles:
                del current_team_roles[role_id]

        current_team_roles.update(teamRolesToAdd)

        doc.reference.update({
            "teamRoles": current_team_roles
        })

def getProjectByIdRepo(id):
    query = projectCollection.where("id","==",id).get()

    project = None

    for doc in query:
        project = doc.to_dict()

    return project

def getEmployeesPartiallyAvailable(id):

    query = employeesCollection.where("organizationId", "==", id).order_by("workingHours").get()

    employeeSorted = []

    for doc in query:
        employee_data = doc.to_dict()
        employeeSorted.append(employee_data)

    return employeeSorted

def assignProposalRepo(assignRequest):

    insertedItm = assignementProposalCollection.document()
    insertedItmId= insertedItm.id

    assignRequest["id"] = insertedItmId

    assignementProposalCollection.add(assignRequest)

    return assignRequest


def getAssignmentProjectRequestRepo(id):
    query = assignementProposalCollection.where("departamentId", "==", id).get()

    assignments = []

    for doc in query:
        currentDoc = doc.to_dict()
        assignments.append(currentDoc)

    return assignments

def closeProjectRepo(id):

    query = projectXemployeeCollection.where("projectId","==",id).get()

    for doc in query:
        doc.reference.update({"isActive":False})

    query = projectStatusCollection.where("projectId","==",id).get()

    for doc in query:
        doc.reference.update({"status" : "Closed"})

def getPastProjectMembersRepo(projectId):

    query = projectXemployeeCollection.where("projectId","==",projectId).where("isActive","==",False    ).get()

    employeeIds= []

    for doc in query:
        currentDoc = doc.to_dict()
        employeeIds.append(currentDoc["employeeId"])

    if not employeeIds:
        raise CustomException(404,"No employees")

    employeesQuery = employeesCollection.where("id", "in", employeeIds).get()

    employeeData = []

    for doc in employeesQuery:
        currentDoc = doc.to_dict()
        currentDoc.pop('password', None)
        employeeData.append(currentDoc)

    return employeeData

def getCurrentProjectMembersRepo(projectId):

    query = projectXemployeeCollection.where("projectId","==",projectId).where("isActive","==",True).get()

    employeeIds= []

    for doc in query:
        currentDoc = doc.to_dict()
        currentDoc.pop('password', None)
        employeeIds.append(currentDoc["employeeId"])

    if not employeeIds:
        raise CustomException(404,"No employees")

    employeesQuery = employeesCollection.where("id", "in", employeeIds).get()

    employeeData = []

    for doc in employeesQuery:
        currentDoc = doc.to_dict()
        currentDoc.pop('password', None)
        employeeData.append(currentDoc)

    return employeeData

def getInfoPastProjectsRepo(employeeId):

    query = projectXemployeeCollection.where("isActive", "==", False).where("employeeId","==",employeeId).get()

    projectIds = []

    for doc in query:
        currentDoc = doc.to_dict()
        projectIds.append(currentDoc["projectId"])

    if not projectIds:
        raise CustomException(404, "No projects")


    projectQuery = projectCollection.where("id", "in", projectIds).get()

    projectData = []

    for doc in projectQuery:
        currentDoc = doc.to_dict()
        projectData.append(currentDoc)

    return projectData


def getInfoCurrentProjectsRepo(employeeId):
    query = projectXemployeeCollection.where("isActive", "==", True).where("employeeId","==",employeeId).get()

    projectIds = []

    for doc in query:
        currentDoc = doc.to_dict()
        projectIds.append(currentDoc["projectId"])

    if not projectIds:
        raise CustomException(404, "No projects")

    projectQuery = projectCollection.where("id", "in", projectIds).get()

    projectData = []

    for doc in projectQuery:
        currentDoc = doc.to_dict()
        projectData.append(currentDoc)

    return projectData