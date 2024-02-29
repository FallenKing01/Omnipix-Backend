from flask import abort
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from Application.Dtos.expect.userExpect import userPostExpect
from Application.Services.userServices import *
from Application.Services.organizationServices import *
from Domain.extension import api,authorizations
from Utils.Exceptions.customException import CustomException

nsUser = Namespace("user", authorizations=authorizations , description="User operations")

@nsUser.route("/create")
class PostUser(Resource):
    @nsUser.expect(userPostExpect)

    def post(self):
        try:

            organization = {
                "name": api.payload["name"],
                "adress": api.payload["adress"],
                "url": api.payload["url"]
            }

            organization=postOrganizationService(organization)
            api.payload["organizationId"] = organization["id"]
            token = postUserService(api.payload)

            return {"Token": token}, 200


        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception as e:
            abort(500, "Something went wrong")

@nsUser.route("/delete/<string:email>")
class DeleteUser(Resource):
    method_decorators = [jwt_required()]
    @nsUser.doc(params={"email": "User email"})
    @nsUser.doc(security="jsonWebToken")
    def delete(self,email):
        try:
            deleteUserService(email)

            return {"message": "User deleted successfully"}, 200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception as e:
            abort(500, "Something went wrong")

@nsUser.route("/updatePassword/<string:email>/<string:newPassword>")
class UpdatePassword(Resource):
    method_decorators = [jwt_required()]
    @nsUser.doc(security="jsonWebToken")
    @nsUser.doc(params={"email": "User email" , "newPassword":"New password"})
    def put(self,email,newPassword):
        try:
            updatePasswordService(email,newPassword)

            return {"message": "User password updated succesfully"}, 200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception as e:
            abort(500, "Something went wrong")






