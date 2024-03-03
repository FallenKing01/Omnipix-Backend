from flask import abort
from flask_restx import Namespace, Resource
from Domain.extension import  authorizations
from Utils.Exceptions.customException import CustomException
from Application.Services.skillService import *
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