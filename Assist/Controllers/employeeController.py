from flask import abort
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from Application.Dtos.expect.employeeExpect import employeePostExpect
from Application.Services.userServices import *
from Domain.extension import api,authorizations
from Utils.Exceptions.customException import CustomException

nsEmployee = Namespace("employee", authorizations=authorizations , description="User operations" )

@nsEmployee.route("/create/<string:organizationId>")
class PostUser(Resource):
    @nsEmployee.doc(params={"organizationId": "Organization id"})
    @nsEmployee.expect(employeePostExpect)

    def post(self , organizationId):
        try:

            api.payload["organizationId"] = organizationId
            token = postUserService(api.payload)

            return {"Token": token}, 200


        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception as e:
            abort(500, "Something went wrong")