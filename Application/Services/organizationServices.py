from Infrastructure.Repositories.OrganizationsRepo import *



def postOrganizationService(organization):

    organization = postOrganizationRepository(organization)

    return organization