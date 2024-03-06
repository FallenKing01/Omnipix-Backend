import uuid
from Application.Dtos.expect.departamentExpect import *
from flask import abort
from flask_restx import Namespace, Resource
from Domain.extension import api, authorizations
from Utils.Exceptions.customException import CustomException
from Application.Services.departamentService import *
nsDepartament = Namespace("departament", authorizations=authorizations, description="Departament operations")

# @nsDepartament.route("/createdirectlywithmanager")
# class PostDepartamentWithManager(Resource):
#     @nsDepartament.expect(departamentPostExpectWithManager)
#     def post(self):
#         try:
#             api.payload["departamentId"]=str(uuid.uuid4())
#             api.payload["departamentManagerId"]=str(uuid.uuid4())
#
#             depart =  postDepartamentServiceWithManager(api.payload)
#
#             return depart
#
#         except CustomException as ce:
#             abort(ce.statusCode, ce.message)
#
#         except Exception:
#             abort(500, "Something went wrong")

@nsDepartament.route("/create")
class PostDepartament(Resource):
    @nsDepartament.expect(departamentPostExpect)
    def post(self):
        try:
            api.payload["departamentId"]=str(uuid.uuid4())
            api.payload["departamentManagerId"]=str(uuid.uuid4())

            depart =  postDepartamentService(api.payload)

            return depart

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsDepartament.route("/skilltodepartament")
class PostSkillToDepartament(Resource):
    @nsDepartament.expect(postDepartamentSkills)
    def post(self):
        try:

            postSkillToDepartamentService(api.payload)

            return {"message":"Skill assigned succesfully to departament"}, 201

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsDepartament.route("/promotedepartamentmanager")
class PromoteToManager(Resource):
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
    def get(self,departamentId):
        try:

            return getSkillsFromDepartamentService(departamentId)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsDepartament.route("/updatemanager")
class UpdateDepartamentManager(Resource):
    @nsDepartament.expect(updateManagerExpect)
    def put(self):
        try:

            updateDepartamentManagerService(api.payload)

            return {"message":"Departament manager updated"}, 201

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")
