from Infrastructure.Repositories.SkillRepo import *
from Utils.Exceptions.customException import CustomException
from Application.Services.organizationServices import getOrganizationService
from Application.Services.userServices import getUserByIdService
from Application.Services.departamentService import getDepartamentManagerByEmployeeIdService
from Infrastructure.Repositories.SkillRepo import getSkillsOfEmployeeRepo

def postSkillService(skill):

    existingOrganization = getOrganizationService(skill["organizationId"])

    if existingOrganization is None:
        raise  CustomException(404,"Organization does not exist")

    existingUser = getUserByIdService(skill["authorId"])

    if existingUser is None:
        raise CustomException(404,"User is not found")

    if existingUser["organizationId"] != skill["organizationId"]:
        raise CustomException(409,"The user is not in organzation provided")

    isManager = getDepartamentManagerByEmployeeIdService(skill["authorId"])

    skill = postSkillRepo(skill)

    return skill

def getSkillOfEmployeeService(employeeId):

    getUserByIdService(employeeId)

    skills = getSkillsOfEmployeeRepo(employeeId)

    return skills

def getSkillService(id):

    skills = getOrganizationSkillsRepo(id)

    return skills

def getSkillByAuthorIdService(id):

    skills = getSkillByAutorIdRepo(id)

    return skills