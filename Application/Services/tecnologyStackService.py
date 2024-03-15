from Application.Services.organizationServices import getOrganizationService
from Infrastructure.Repositories.technologyStackRepo import *


def createTecnologyStackService(tecnology):
    getOrganizationService(tecnology["organizationId"])
    return postTechnologyStackRepo(tecnology)
