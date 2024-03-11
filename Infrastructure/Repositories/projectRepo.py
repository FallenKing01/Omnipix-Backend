from Domain.extension import projectCollection
from Infrastructure.Repositories.ProjectManagerRepo import updateProjectsOfManager

def postProjectRepo(project):

    insertedItm = projectCollection.document()
    insertedItmId = insertedItm.id

    updateProjects = {
        "employeeId":project["employeeId"],
        "projectId":insertedItmId
    }

    updateProjectsOfManager(updateProjects)

    project["id"] = insertedItmId

    projectCollection.add(project)

    return project