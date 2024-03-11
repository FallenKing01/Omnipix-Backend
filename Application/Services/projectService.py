from Infrastructure.Repositories.projectRepo import *
from Application.Services.organizationServices import getOrganizationService
from Utils.Exceptions.customException import CustomException
def getProjectByIdService(id):
    isProject = getProjectByIdRepo(id)

    if isProject is None:
        raise CustomException(404,"Project not found")

    return isProject

def postProjectService(project):

    getOrganizationService(project["organizationId"])

    project = postProjectRepo(project)

    return project

def updateProjectService(project):

    getProjectByIdService(project["projectId"])
    updateProjectRepo(project)