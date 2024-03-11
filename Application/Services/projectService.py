from Infrastructure.Repositories.projectRepo import *
from Application.Services.organizationServices import getOrganizationService
def postProjectService(project):

    getOrganizationService(project["organizationId"])

    project = postProjectRepo(project)

    return project
