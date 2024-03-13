from flask import abort
from flask_restx import Namespace, Resource
from Domain.extension import  authorizations
from Utils.Exceptions.customException import CustomException
from Application.Services.skillService import *
from Application.Services.departamentService import *
from Application.Dtos.expect.departamentManagerExpect import *
nsDepartamentManager = Namespace("departamentmanager",authorizations=authorizations,description="Departament manager operations")

@nsDepartamentManager.route("/createskill")
class PostSkill(Resource):
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
    def get(self,id):

        try:
            managers = getDepartamentManagerWithNoDepartamentService(id)

            return managers

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsDepartamentManager.route("/departamentallocationproposal/<string:departamentId>")
class GetAllocationsProposals(Resource):
    def get(self,departamentId):

        try:
            proposals = getDepartamentAllocationProposalRepo(departamentId)

            return proposals

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsDepartamentManager.route("/departamentdeallocationonproposal/<string:departamentId>")
class GetDeallocationsProposals(Resource):
    def get(self,departamentId):

        try:
            proposals = getDealocationProposalRepo(departamentId)

            return proposals

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsDepartamentManager.route("/getdepartamentsfromorganization/<string:organizationId>")
class GetDepartamentsFromOrganization(Resource):
    def get(self,organizationId):

        try:
            return getDepartamentsRepo(organizationId)


        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsDepartamentManager.route("/assignskilldirectly")
class AssignSkillDirectly(Resource):
    @nsDepartamentManager.expect(assignSkillDirectlyExpect)

    def post(self):

        try:
            return assignSkillDirectlyRepo(api.payload)


        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")