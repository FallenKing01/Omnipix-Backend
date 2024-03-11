from Domain.extension import projectCollection,projectStatusCollection,employeesCollection
from Infrastructure.Repositories.ProjectManagerRepo import updateProjectsOfManager
from datetime import datetime

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




