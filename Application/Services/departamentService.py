from Utils.Exceptions.customException import CustomException
from Infrastructure.Repositories.DepartamentRepo import *
from Application.Services.organizationServices import getOrganizationService
from Application.Services.userServices import getUserByIdService
def getDepartamentManagerByEmployeeIdService(id):

    isManager = getDepartamentManagerByEmployeeIdRepo(id)

    if isManager is None:
        raise CustomException(404, "The employee is not departament manager!")

    return isManager

def postDepartamentServiceWithManager(depart):

    existingOrganization = getOrganizationService(depart["organizationId"])

    if existingOrganization is None:
        raise CustomException(404, "Organization not found")

    existingEmployee = getUserByIdService(depart["employeeId"])

    if existingEmployee is None:
        raise CustomException(404, "The employee does not exist")

    isManager = getDepartamentManagerByEmployeeIdRepo(depart["employeeId"])

    if isManager is not None:
        raise CustomException(409, "The user is already manager")

    depart = postDepartamentWithManagerRepo(depart)

    return depart

def postDepartamentService(depart):

    existingOrganization = getOrganizationService(depart["organizationId"])

    if existingOrganization is None:
        raise CustomException(404, "Organization not found")

    depart = postDepartamentRepo(depart)

    return depart

def getDepartamentByIdService(id):

    departament = getDepartmentByIdRepo(id)

    if departament is None:
        raise CustomException("Departament does not exist")

    return departament

def promoteToDepartamentManagerService(user):

    existingEmployee = getUserByIdService(user["employeeId"])

    if existingEmployee is None:
        raise CustomException(404, "The employee does not exist")

    isManager = getDepartamentManagerByEmployeeIdRepo(user["employeeId"])

    if isManager is not None:
        raise CustomException(409, "The user is already manager")

    updateDepartamentManager(user)