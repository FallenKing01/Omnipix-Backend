from Application.Dtos.expect.departamentExpect import *
from flask import abort
from flask_restx import Namespace, Resource
from Domain.extension import api, authorizations
from Utils.Exceptions.customException import CustomException
from Application.Services.departamentService import *
createManager = Namespace("test", authorizations=authorizations, description="Departament operations")
from Application.Services.createDepartService import postDepartManService

nsTest = Namespace("test", authorizations=authorizations, description="Test operations")

@nsTest.route("/createdepartamentmanager")
class PostDepartamentManager(Resource):
    @nsTest.expect(postDepartamentManagerExpect)
    def post(self):
        try:

            depart =  postDepartManService(api.payload)

            return depart

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")