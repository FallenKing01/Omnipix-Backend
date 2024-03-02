from Utils.Exceptions.customException import CustomException
from Infrastructure.Repositories.departamentRepo import *
from Application.Services.organizationServices import getOrganizationService
from Application.Services.userServices import getUserByIdService
def getDepartamentByEmployeeIdService(id):

    isManager = getDepartamentByEmployeeIdRepo(id)

    return isManager
def postDepartamentService(depart):

    existingOrganization = getOrganizationService(depart["organizationId"])

    if existingOrganization is None:
        raise CustomException(404, "Organization not found")

    existingEmployee = getUserByIdService(depart["employeeId"])

    if existingEmployee is None:
        raise CustomException(404, "The employee does not exist")

    isManager = getDepartamentByEmployeeIdService(depart["employeeId"])

    if isManager is not None:
        raise CustomException(409, "The user is already manager")

    depart = postDepartamentRepo(depart)

    return depart