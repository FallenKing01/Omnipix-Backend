from Infrastructure.Repositories.SkillRepo import *
from Utils.Exceptions.customException import CustomException
from Application.Services.organizationServices import getOrganizationService
from Application.Services.userServices import getUserByIdService
from Utils.getDepartamentById import getDepartamentManagerByEmployeeIdService
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

    getDepartamentManagerByEmployeeIdService(skill["authorId"])

    skill = postSkillRepo(skill)

    return skill


def getSkillOfEmployeeService(employeeId):

    getUserByIdService(employeeId)

    skills = getSkillsOfEmployeeRepo(employeeId)

    return skills


def getSkillByIdService(id):

    skills = getOrganizationSkillsRepo(id)

    if not skills:
        CustomException(404,"Skills not found")

    return skills


def getSkillByAuthorIdService(id):

    skills = getSkillByAutorIdRepo(id)

    return skills


def updateSkillService(skill):

    existSkill = getSkillByIdRepo(skill["skillId"])

    if existSkill is None:
        raise CustomException(404, "Skill not found")


    return updateSkillRepo(skill)
