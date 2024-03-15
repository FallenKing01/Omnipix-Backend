from Domain.extension import technologyStackCollection,customTeamRoleCollection,dealocationProposalCollection,skillXprojectCollection,projectCollection,projectManagerCollection,assignementProposalCollection,projectStatusCollection,employeesCollection,projectXemployeeCollection
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

def getProjectsFromOrganizationRepo(organizationId):
    query = projectCollection.where("organizationId", "==", organizationId).get()

    finalProjects = []

    for doc in query:
        project = doc.to_dict()

        teamRolesIds = []
        teamRolesValues = []

        for key, value in project["teamRoles"].items():
            teamRolesIds.append(key)
            teamRolesValues.append(value)

        if teamRolesIds:
            queryRoles = customTeamRoleCollection.where("id", "in", teamRolesIds).get()
            toInsertRoles = []

            for docRoles, value in zip(queryRoles, teamRolesValues):
                currentDoc = docRoles.to_dict()
                currentDoc["value"] = value
                toInsertRoles.append(currentDoc)

            project["teamRoles"] = toInsertRoles

        technologyStackId = []

        for valueTec in project["technologyStack"]:
            technologyStackId.append(valueTec)

        if technologyStackId:
            queryTech = technologyStackCollection.where("id", "in", technologyStackId).get()
            technologyStackToReturn = []

            for docTechnology in queryTech:
                technologyStackToReturn.append(docTechnology.to_dict())

            project["technologyStack"] = technologyStackToReturn

        finalProjects.append(project)

    if not finalProjects:
        raise CustomException(404, "No projects")

    return finalProjects


def getProjectsForDepartamentManagerEmployeeRepo(departamentId):
    queryEmployee = employeesCollection.where("departamentId", "==", departamentId).get()
    employeeIds = []

    for doc in queryEmployee:
        currentDoc = doc.to_dict()
        currentDoc.pop('password', None)
        employeeIds.append(currentDoc["id"])

    if not employeeIds:
        raise CustomException(404, "Employees not found in department")

    projectIds = []
    queryProjectEmployee = projectXemployeeCollection.where("employeeId", "in", employeeIds).get()

    for doc in queryProjectEmployee:
        currentDoc = doc.to_dict()
        projectIds.append(currentDoc["projectId"])

    if not projectIds:
        raise CustomException(404, "Projects not found for members of your department")

    projectsData = []
    queryProject = projectCollection.where("id", "in", projectIds).get()

    for doc in queryProject:
        projectData = doc.to_dict()

        # Fetch complete technology objects
        technologyIds = projectData.get("technologyStack", [])
        technologyData = []
        if technologyIds:
            technologyQuery = technologyStackCollection.where("id", "in", technologyIds).get()
            for techDoc in technologyQuery:
                technologyData.append(techDoc.to_dict())
            projectData["technologyStack"] = technologyData

        teamRolesData = {}
        teamRoles = projectData.get("teamRoles", {})
        if teamRoles:
            for roleId, roleValue in teamRoles.items():
                roleDoc = customTeamRoleCollection.document(roleId).get()
                roleData = roleDoc.to_dict()
                roleData["value"] = roleValue
                teamRolesData[roleId] = roleData
            projectData["teamRoles"] = teamRolesData

        projectsData.append(projectData)

    if not projectsData:
        raise CustomException(404, "Projects not found")

    return projectsData




def getProjectDetailsRepo(projectId):

    query = projectCollection.where("id","==",projectId).get()

    project = None

    for doc in query:
        project = doc.to_dict()

    if project is None:
        raise CustomException(404,"There is no project with this id")

    teamRolesIds = []
    teamRolesValues = []

    for key, value in project["teamRoles"].items():
        teamRolesIds.append(key)
        teamRolesValues.append(value)

    if teamRolesIds:
        query = customTeamRoleCollection.where("id","in",teamRolesIds).get()
        toInsertRoles = []

        for doc, value in zip(query, teamRolesValues):
            currentDoc = doc.to_dict()
            # Adding the value from teamRolesValues to currentDoc
            currentDoc["value"] = value
            toInsertRoles.append(currentDoc)
        project["teamRoles"] = toInsertRoles

    technologyStackId = []
    technologyStackToReturn = []

    for value in project["technologyStack"]:
        technologyStackId.append(value)
    print(technologyStackId)

    if technologyStackId:
        query = technologyStackCollection.where("id","in",technologyStackId).get()

        for doc in query:
            currentDoc = doc.to_dict()
            technologyStackToReturn.append(currentDoc)

        project["technologyStack"] = technologyStackToReturn

    return project


def projectToDeleteRepo(projectId):
        query = projectCollection.where("id", "==", projectId).get()
        for doc in query:
            doc.reference.delete()

        query = projectManagerCollection.where("projectId", "==", projectId).get()
        for doc in query:
            doc.reference.delete()

        query = projectStatusCollection.where("projectId", "==" ,projectId).get()
        for doc in query:
            doc.reference.delete()

        query = skillXprojectCollection.where("projectId","==",projectId).get()

        for doc in query:
            doc.reference.delete()

        query = projectXemployeeCollection.where("projectId","==",projectId).get()


        for doc in query:
            doc.reference.delete()

        query = assignementProposalCollection.where("projectId","==",projectId).get()

        for doc in query:
            doc.reference.delete()

        query = dealocationProposalCollection.where("projectId","==",projectId).get()

        for doc in query:
            doc.reference.delete()








