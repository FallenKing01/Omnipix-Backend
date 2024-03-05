from flask import abort
from flask_restx import Namespace, Resource

from Application.Dtos.expect.employeeExpect import *
from Application.Services.userServices import *
from Domain.extension import api,authorizations
from Utils.Exceptions.customException import CustomException
from Application.Services.assignSkillService import postSkillWithEndorsmentService

nsEmployee = Namespace("employee", authorizations=authorizations , description="User operations" )

@nsEmployee.route("/")
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

        except Exception as e:
            abort(500, "Something went wrong")