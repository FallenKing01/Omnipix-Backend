from flask import abort
from flask_restx import Namespace, Resource
from Domain.extension import authorizations
from Utils.Exceptions.customException import CustomException
from Application.Services.skillService import *
from Application.Services.departamentService import *
from Application.Dtos.expect.departamentManagerExpect import *
from flask_jwt_extended import jwt_required
nsDepartamentManager = Namespace("departamentmanager", authorizations=authorizations,
                                 description="Departament manager operations")


@nsDepartamentManager.route("/createskill")
class PostSkill(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartamentManager.doc(security="jsonWebToken")
    @nsDepartamentManager.expect(skillPostExpect)
    def post(self):
        try:

            skill = postSkillService(api.payload)

            return skill

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsDepartamentManager.route("/getskills/<string:organizationId>")
class GetSkills(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartamentManager.doc(security="jsonWebToken")
    @nsDepartamentManager.doc(params={'organizationId': 'The ID of the organization for which to retrieve skills'})
    def get(self, organizationId):

        try:
            skills = getSkillByIdService(organizationId)
            return skills

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsDepartamentManager.route("/ownedskills/<string:authorId>")
class GetSkillsCreatedByDepartamentManager(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartamentManager.doc(security="jsonWebToken")
    @nsDepartamentManager.doc(params={'authorId': 'The id of man who made the skill'})
    def get(self, authorId):

        try:
            skills = getSkillByAuthorIdService(authorId)

            return skills

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsDepartamentManager.route("/editskill")
class UpdateSkill(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartamentManager.doc(security="jsonWebToken")
    @nsDepartamentManager.expect(skillUpdateExpect)
    def put(self):

        try:
            updatedSkill = updateSkillService(api.payload)

            return updatedSkill

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsDepartamentManager.route("/managersnodepartament/<string:id>")
class GetManagersNoDepartament(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartamentManager.doc(security="jsonWebToken")
    def get(self, id):

        try:
            managers = getDepartamentManagerWithNoDepartamentService(id)

            return managers

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsDepartamentManager.route("/departamentallocationproposal/<string:departamentId>")
class GetAllocationsProposals(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartamentManager.doc(security="jsonWebToken")
    def get(self, departamentId):

        try:
            proposals = getDepartamentAllocationProposalRepo(departamentId)

            return proposals

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsDepartamentManager.route("/departamentdeallocationonproposal/<string:departamentId>")
class GetDeallocationsProposals(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartamentManager.doc(security="jsonWebToken")
    def get(self, departamentId):

        try:
            proposals = getDealocationProposalRepo(departamentId)

            return proposals

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsDepartamentManager.route("/getdepartamentsfromorganization/<string:organizationId>")
class GetDepartamentsFromOrganization(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartamentManager.doc(security="jsonWebToken")
    def get(self, organizationId):

        try:
            return getDepartamentsRepo(organizationId)


        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsDepartamentManager.route("/assignskilldirectly")
class AssignSkillDirectly(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartamentManager.doc(security="jsonWebToken")
    @nsDepartamentManager.expect(assignSkillDirectlyExpect)
    def post(self):

        try:
            return assignSkillDirectlyRepo(api.payload)


        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsDepartamentManager.route("/chartdiagramspecialistlevel/<string:departamentId>/<string:skillId>")
class ChartSpecialistLevel(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartamentManager.doc(security="jsonWebToken")
    def get(self, departamentId, skillId):

        try:
            return getChartSkillsRepo(departamentId, skillId)


        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsDepartamentManager.route("/kickemployeefromdepartament/<string:employeeId>")
class KickEmployeeFromDepartament(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartamentManager.doc(security="jsonWebToken")
    def put(self, employeeId):

        try:
            return kickEmployeeFromDepartamentRepo(employeeId)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsDepartamentManager.route("/deleteskillfromdepartament/<string:skillId>/<string:departamentId>")
class deleteSkillFromDepartament(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartamentManager.doc(security="jsonWebToken")
    def delete(self, skillId,departamentId):

        try:

            deleteSkillFromDepartamentRepo(skillId,departamentId)

            return {"message":"Skill deleted from departament"}


        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsDepartamentManager.route("/deleteskillfromorganization/<string:skillId>/<string:organizationId>")
class deleteSkill(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartamentManager.doc(security="jsonWebToken")
    def delete(self, skillId,organizationId):

        try:

            deleteSkillPermanentRepo(skillId,organizationId)

            return {"message": "Skill deleted from organization"}

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsDepartamentManager.route("/demotedepartamentmanager/<string:employeeId>")
class DemoteDepartamentManager(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartamentManager.doc(security="jsonWebToken")
    def delete(self, employeeId):

        try:
            demoteDepartamentManagerRepo(employeeId)

            return {"message":"Departament manager demoted"}

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")
@nsDepartamentManager.route("/getproposalsforskills/<string:departamentId>")
class GetProposalsForSkills(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartamentManager.doc(security="jsonWebToken")
    def get(self, departamentId):

        try:
            proposals = getProposalForSkillsFromDepartamentRepo(departamentId)

            return proposals

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

