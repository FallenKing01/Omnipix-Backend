import uuid

from flask_jwt_extended import jwt_required

from Application.Dtos.expect.departamentExpect import *
from flask import abort
from flask_restx import Namespace, Resource
from Domain.extension import api, authorizations
from Utils.Exceptions.customException import CustomException
from Application.Services.departamentService import *
nsDepartament = Namespace("departament", authorizations=authorizations, description="Departament operations")



@nsDepartament.route("/createdirectlywithmanagerADDITIONAL")
class PostDepartamentWithManager(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartament.doc(security="jsonWebToken")
    @nsDepartament.expect(departamentPostExpectWithManager)
    def post(self):
        try:
            api.payload["departamentId"]=str(uuid.uuid4())
            api.payload["departamentManagerId"]=str(uuid.uuid4())

            depart =  postDepartamentServiceWithManager(api.payload)

            return depart

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsDepartament.route("/createADDITIONAL")
class PostDepartament(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartament.doc(security="jsonWebToken")
    @nsDepartament.expect(departamentPostExpect)
    def post(self):
        try:
            api.payload["departamentId"]=str(uuid.uuid4())
            api.payload["departamentManagerId"]=str(uuid.uuid4())

            depart =  postDepartamentServiceADDITIONAL(api.payload)

            return depart

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsDepartament.route("/create")
class PostDepartament(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartament.doc(security="jsonWebToken")
    @nsDepartament.expect(departamentPostExpect)
    def post(self):
        try:

            depart =  postDepartamentService(api.payload)

            return depart

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsDepartament.route("/skilltodepartament")
class PostSkillToDepartament(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartament.doc(security="jsonWebToken")
    @nsDepartament.expect(postDepartamentSkills)
    def post(self):
        try:

            postSkillToDepartamentService(api.payload)

            return {"message":"Skill assigned succesfully to departament"}, 201

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsDepartament.route("/promotedepartamentmanagerADDITIONAL")
class PromoteToManager(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartament.doc(security="jsonWebToken")
    @nsDepartament.expect(promoteDepartamentManager)
    def put(self):
        try:

            promoteToDepartamentManagerService(api.payload)

            return {"message":"Promoted to departament manager successfully"}, 201

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsDepartament.route("/skillsofdepartament/<string:departamentId>")
class PostDepartament(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartament.doc(security="jsonWebToken")
    def get(self,departamentId):
        try:

            return getSkillsFromDepartamentService(departamentId)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsDepartament.route("/updatemanager")
class UpdateDepartamentManager(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartament.doc(security="jsonWebToken")
    @nsDepartament.expect(updateManagerExpect)
    def put(self):
        try:

            updateDepartamentManagerService(api.payload)

            return {"message":"Departament manager updated"}, 201

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsDepartament.route("/updatenameofdepartament")
class UpdateDepartamentName(Resource):
    @nsDepartament.expect(updateDepartamentNameExpect)
    def put(self):
        # method_decorators = [jwt_required()]
        # @nsDepartament.doc(security="jsonWebToken")
        try:

            updateNameOfDepartamentService(api.payload)

            return {"message":"Departament name updated"}, 201

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsDepartament.route("/deletedepartament/<string:departamentId>")
class DeleteDepartament(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartament.doc(security="jsonWebToken")
    def delete(self,departamentId):
        try:
            deleteDepartamentService(departamentId)

            return {"message":"Departament was deleted"}, 202

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")



@nsDepartament.route("/firstpromotedepartamentmanager")
class PromoteFirstTimeToDepartamentManager(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartament.doc(security="jsonWebToken")
    @nsDepartament.expect(promoteDepartamentManager)
    def put(self):
        try:

            firstDepartamentManagerPromotionService(api.payload)

            return {"message":"The employee was promoted"}, 201

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsDepartament.route("/acceptprojectproposal")
class AcceptProjectProposal(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartament.doc(security="jsonWebToken")
    @nsDepartament.expect(acceptProposalExpect)
    def post(self):
        try:

            return acceptProjectProposalService(api.payload)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsDepartament.route("/declineprojectproposal/<string:proposalId>")
class DeclineProposal(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartament.doc(security="jsonWebToken")
    def delete(self,id):
        try:

            declineProposalProjectRepo(id)

            return {"message":"Declined a employee succesfully"}

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsDepartament.route("/declinedealocationproposal/<string:id>")
class DeclineDealocationProposal(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartament.doc(security="jsonWebToken")
    def delete(self,id):
        try:

            declineDealocationProposalService(id)

            return {"message":"Declined a dealocation proposal succesfully"}

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsDepartament.route("/createadealocationproposal")
class CreateDealocationProposal(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartament.doc(security="jsonWebToken")
    @nsDepartament.expect(dealocationProposalExpect)
    def post(self):
        try:

            return dealocationProposalService(api.payload)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsDepartament.route("/acceptdealocatioproposal")
class AcceptDealocationProposal(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartament.doc(security="jsonWebToken")
    @nsDepartament.expect(acceptDealocationProposal)
    def put(self):
        try:

            return acceptDealocationProposalService(api.payload)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsDepartament.route("/getnamedepartament/<string:employeeId>")
class GetNameDepartament(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartament.doc(security="jsonWebToken")
    def get(self,employeeId):
        try:

            return getDepartamentNameRepo(employeeId)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsDepartament.route("availableskills/<string:departamentId>/<string:organizationId>")
class availableSkillsInDepartament(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartament.doc(security="jsonWebToken")
    def get(self,departamentId,organizationId):
        try:

            return getAvailableDepartamentSkills(departamentId,organizationId)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsDepartament.route("/notassignedskills/<string:departamentId>/<string:organizationId>")
class notAssignedDepartamentSkills(Resource):
    # method_decorators = [jwt_required()]
    # @nsDepartament.doc(security="jsonWebToken")
    def get(self,departamentId,organizationId):
        try:

            return getNotAssignedSkillsOfDepartamentRepo(departamentId,organizationId)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")