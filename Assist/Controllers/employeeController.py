from flask import abort,jsonify
from flask_restx import Namespace, Resource

from Application.Dtos.expect.employeeExpect import *
from Application.Services.userServices import *
from Domain.extension import api,authorizations
from Utils.Exceptions.customException import CustomException
from Application.Services.assignSkillService import postSkillWithEndorsmentService
from Application.Services.skillService import getSkillOfEmployeeService

nsEmployee = Namespace("employee", authorizations=authorizations , description="User operations" )

@nsEmployee.route("/create")
class PostUser(Resource):
    @nsEmployee.expect(employeePostExpect)

    def post(self):
        try:

            token,x = postUserService(api.payload)

            return {"Token": token}, 200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsEmployee.route("/postskillinproject")
class PostProjectSkill(Resource):
    @nsEmployee.expect(postProjectSkill)

    def post(self):
        try:
            skill = postSkillInProjectService(api.payload)

            return skill,200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsEmployee.route("/getskills/<string:userId>")
class GetUserSkills(Resource):

    def get(self,userId):
        try:

            return getSkillOfEmployeeService(userId)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsEmployee.route("/assignskill")
class AssignSkill(Resource):
    @nsEmployee.expect(assignSkill)
    def post(self):
        try:
            data = nsEmployee.payload

            endorsements = data.get('endorsements', [])
            postSkillWithEndorsmentService(data,endorsements)

            return {'message': 'Skill assigned successfully'}, 200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception as e:
            abort(500, "Something went wrong")

@nsEmployee.route("/assigndepartament")
class AssignDepartament(Resource):
    @nsEmployee.expect(assignDepartament)
    def put(self):
        try:
            assignUserToDepartamentService(api.payload)

            return {'message': 'Departament assigned successfully'}, 200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsEmployee.route("/roles/<string:id>")
class GetUserRoles(Resource):
    def get(self,id):
        try:
            roles = getUserRolesService(id)

            return roles,200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsEmployee.route("/deleteskillfromproject/<string:id>")
class DeleteSkillFromProject(Resource):
    def delete(self,id):
        try:
            deleteSkillFromProjectService(id)

            return {"message":"Deleted succesfully"},200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsEmployee.route("/getskillsfromproject/<string:id>")
class GetSkillsFromProject(Resource):
    def get(self,id):
        try:
            skills = getSkillsFromProjectService(id)

            return skills

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsEmployee.route("/organizationemployees/<string:id>")
class GetOrganizationEmployees(Resource):
    def get(self,id):
        try:
            employees = getOrganizationEmployeesService(id)

            return employees

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsEmployee.route("/departamentemployees/<string:id>")
class GetDepartamentEmployees(Resource):
    def get(self,id):
        try:
            employees = getDepartamentEmployeeService(id)

            return employees

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsEmployee.route("/inactiveskils/<string:departamentId>")
class GetInactiveSkills(Resource):
    def get(self,departamentId):
        try:
            skills = getInactiveAssignSkills(departamentId)

            return skills

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")




@nsEmployee.route("/activateaskill/<string:skillId>")
class GetInactiveSkills(Resource):
    def get(self,skillId):
        try:
            acceptProposalForSkill(skillId)

            return {"message":"Skill accepted succesfuly"},200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsEmployee.route("/activateaskill/<string:skillId>")
class ActivateSkill(Resource):
    def put(self,skillId):
        try:
            acceptProposalForSkill(skillId)

            return {"message":"Skill accepted succesfuly"},200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsEmployee.route("/declineproposalskill/<string:skillId>")
class DeclineSkill(Resource):
    def delete(self,skillId):
        try:
            declineProposalForSkill(skillId)

            return {"message":"Skill declined succesfuly"},200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsEmployee.route("/getendorsmentofskill/<string:assignedSkillId>")
class GetEndorsmentOfSkill(Resource):
    def get(self, assignedSkillId):
        try:
            endorsment = getEndorsmentOfSkill(assignedSkillId)

            return endorsment

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsEmployee.route("/info/<string:employeeId>")
class GetInfoParticularyEmployee(Resource):
    def get(self, employeeId):
        try:
            return getInfoAboutUserRepo(employeeId)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsEmployee.route("/employeesnodepartament/<string:organizationId>")
class GetEmployeesNotInDepartament(Resource):
    def get(self, organizationId):
        try:
            return getEmployeesNoDepartament(organizationId)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")