from Application.Dtos.expect.departamentExpect import *
from flask import abort
from flask_restx import Namespace, Resource
from Domain.extension import api, authorizations
from Utils.Exceptions.customException import CustomException
from flask_jwt_extended import jwt_required
from Application.Services.departamentService import *
createManager = Namespace("test", authorizations=authorizations, description="Departament operations")
from Application.Services.createDepartService import postDepartManService

nsTest = Namespace("departamentpromotion", authorizations=authorizations, description="departament promotion")

@nsTest.route("/")
class PostDepartamentManager(Resource):
    # method_decorators = [jwt_required()]
    # @nsTest.doc(security="jsonWebToken")
    @nsTest.expect(postDepartamentManagerExpect)
    def post(self):
        try:

            depart =  postDepartManService(api.payload)

            return depart

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")