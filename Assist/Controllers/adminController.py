from flask import abort
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from Application.Dtos.expect.adminExpect import userPostExpect
from Application.Services.userServices import *
from Application.Services.organizationServices import *
from Domain.extension import api, authorizations
from Utils.Exceptions.customException import CustomException

nsAdmin = Namespace("admin", authorizations=authorizations, description="Admin operations")


@nsAdmin.route("/create")
class PostUser(Resource):
    @nsAdmin.expect(userPostExpect)
    def post(self):
        try:

            organization = {
                "name": api.payload["organizationName"],
                "adress": api.payload["adress"],
                "url": api.payload["url"]
            }

            organization = postOrganizationService(organization)
            api.payload["organizationId"] = organization["id"]
            api.payload.pop("url")
            api.payload.pop("adress")
            api.payload.pop("organizationName")
            token = postUserService(api.payload)

            return {"Token": token}, 200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsAdmin.route("/delete/<string:email>")
class DeleteUser(Resource):
    method_decorators = [jwt_required()]

    @nsAdmin.doc(params={"email": "User email"})
    @nsAdmin.doc(security="jsonWebToken")
    def delete(self, email):
        try:
            deleteUserService(email)

            return {"message": "User deleted successfully"}, 200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsAdmin.route("/updatePassword/<string:email>/<string:newPassword>")
class UpdatePassword(Resource):
    method_decorators = [jwt_required()]

    @nsAdmin.doc(security="jsonWebToken")
    @nsAdmin.doc(params={"email": "User email", "newPassword": "New password"})
    def put(self, email, newPassword):
        try:
            updatePasswordService(email, newPassword)

            return {"message": "User password updated succesfully"}, 200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")
