from Utils.Exceptions.customException import CustomException
from Infrastructure.Repositories.UserRepo import getUserByIdRepository
from Infrastructure.Repositories.assignedSkillRepo import postSkillWithEndorsmentRepo

def postSkillWithEndorsmentService(skillAssigned,endorsementsAssigned):

    employeeToAssign = getUserByIdRepository(skillAssigned["employeeId"])

    if employeeToAssign is None:
        raise CustomException(404,"Employee not found")

    skillAssigned["departamentId"] = employeeToAssign["departamentId"]

    skillAssigned,endorsementsAssigned = postSkillWithEndorsmentRepo(skillAssigned,endorsementsAssigned)

    return skillAssigned,endorsementsAssigned


