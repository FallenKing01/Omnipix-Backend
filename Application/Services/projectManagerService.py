from Infrastructure.Repositories.ProjectManagerRepo import *
from Application.Services.userServices import getUserByIdService
from Application.Services.organizationServices import getOrganizationService
def postProjectManagerService(id):

    getUserByIdService(id)

    postProjectManagerRepo(id)

def searchUserService(employee):

    getOrganizationService(employee["organizationId"])

    return searchForUserRepo(employee)