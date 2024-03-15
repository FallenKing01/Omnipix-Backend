from Infrastructure.Repositories.OrganizationsRepo import *
from Utils.Exceptions.customException import CustomException


def postOrganizationService(organization):
    return postOrganizationRepository(organization)


def getOrganizationService(id):

    organization = getOrganizationByIdRepository(id)

    if organization is None:
        raise CustomException(404, "Organization not found")

    return organization
