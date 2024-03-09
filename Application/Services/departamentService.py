from Utils.Exceptions.customException import CustomException
from Infrastructure.Repositories.DepartamentRepo import *
from Infrastructure.Repositories.DepartamentRepo import createDepartManRepo
from Infrastructure.Repositories.skillXdepartamentRepo import *
from Infrastructure.Repositories.SkillRepo import getSkillByIdRepo
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

def postDepartamentServiceADDITIONAL(depart):

    existingOrganization = getOrganizationService(depart["organizationId"])

    if existingOrganization is None:
        raise CustomException(404, "Organization not found")

    depart = postDepartamentRepoADDITIONAL(depart)

    return depart

def getDepartamentByIdService(id):

    departament = getDepartmentByIdRepo(id)

    if departament is None:
        raise CustomException(404,"Departament does not exist")

    return departament

#devine pentru prima data manager
def promoteToDepartamentManagerService(user):

    existingEmployee = getUserByIdService(user["employeeId"])

    if existingEmployee is None:
        raise CustomException(404, "The employee does not exist")

    isManager = getDepartamentManagerByEmployeeIdRepo(user["employeeId"])

    if isManager is not None:
        raise CustomException(409, "The user is already manager")

    updateSecondTimeManagerOfDepartamentRepo(user)

def postSkillToDepartamentService(skill):

    existSkill = getSkillByIdRepo(skill["skillId"])

    if existSkill is None:
        raise CustomException(404,"Skill is not found")


    getDepartamentByIdService(skill["departamentId"])

    skill = postSkillToDepartamentRepo(skill)

    return skill

def getSkillsFromDepartamentService(departamentId):

    skills = getSkillsFromDepartmentRepo(departamentId)

    return skills

#Se schimba managerul pe departament era deja cineva acum e altu!
def updateDepartamentManagerService(departament):

    existDepartament = getDepartamentByIdService(departament["departamentId"])
    existUser = getUserByIdService(departament["employeeId"])

    if existDepartament["organizationId"] != existUser["organizationId"]:
        raise CustomException(409,"User and departament are not in the same organization")

    isManager = getDepartamentManagerByEmployeeIdRepo(departament["employeeId"])

    if isManager is not None:
        raise CustomException(409, "The user is already manager")

    updateDepartamentManagerRepo(departament)


def updateNameOfDepartamentService(departament):

    getDepartamentByIdService(departament["departamentId"])

    updateNameOfDepartamentRepo(departament)



def postDepartManService(employee):
    getUserByIdService(employee["employeeId"])

    createDepartManRepo(employee)

    return employee

def deleteDepartamentService(id):

    getDepartamentByIdService(id)
    deleteDepartamentRepo(id)

def postDepartamentService(departament):
    getOrganizationService(departament["organizationId"])

    departament = postDepartamentRepo(departament)

    return departament

def firstDepartamentManagerPromotionService(depart):

    existDepartament = getDepartmentByIdRepo(depart["departamentId"])

    if existDepartament is None:
        raise  CustomException(404,"Departament does not exist")

    getUserByIdService(depart["employeeId"])

    firstDepartamentManagerPromotionRepo(depart)

def getDepartamentManagerWithNoDepartamentService(id):

    getOrganizationService(id)

    managers = getDepartamentManagerWithNoDepartament(id)

    return managers