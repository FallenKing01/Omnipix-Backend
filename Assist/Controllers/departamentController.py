import uuid
from Application.Dtos.expect.departamentExpect import *
from flask import abort
from flask_restx import Namespace, Resource
from Domain.extension import api, authorizations
from Utils.Exceptions.customException import CustomException
from Application.Services.departamentService import *
nsDepartament = Namespace("departament", authorizations=authorizations, description="Departament operations")

@nsDepartament.route("/createdirectlywithmanager")
class PostDepartamentWithManager(Resource):
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

@nsDepartament.route("/promotedepartamentmanager")
class PostDepartament(Resource):
    @nsDepartament.expect(promoteDepartamentManager)
    def put(self):
        try:

            promoteToDepartamentManagerService(api.payload)

            return {"message":"Promoted to departament manager successfully"}, 201

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")



