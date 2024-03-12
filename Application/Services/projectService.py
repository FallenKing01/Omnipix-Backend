from Infrastructure.Repositories.projectRepo import *
from Application.Services.organizationServices import getOrganizationService
from Utils.Exceptions.customException import CustomException
from Application.Services.departamentService import getDepartamentByIdService
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

def assignProposalService(assignRequest):

    getProjectByIdService(assignRequest["projectId"])
    getDepartamentByIdService(assignRequest["departamentId"])

    return assignProposalRepo(assignRequest)

def getAssignmentProjectRequestService(id):

    return getAssignmentProjectRequestRepo(id)