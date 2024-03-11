from Application.Services.organizationServices import getOrganizationService
from Infrastructure.Repositories.technologyStackRepo import *

def createTecnologyStackService(tecnology):

    getOrganizationService(tecnology["organizationId"])

    tecnology = postTechnologyStackRepo(tecnology)

    return tecnology
