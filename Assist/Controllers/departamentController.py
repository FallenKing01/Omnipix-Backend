import uuid
from Application.Dtos.expect.departamentExpect import departamentPostExpect
from flask import abort
from flask_restx import Namespace, Resource
from Domain.extension import api, authorizations
from Utils.Exceptions.customException import CustomException
from Application.Services.departamentService import postDepartamentService
nsDepartament = Namespace("departament", authorizations=authorizations, description="Admin operations")

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
