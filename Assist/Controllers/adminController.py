from flask import abort
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from Application.Dtos.expect.adminExpect import *
from Application.Services.userServices import *
from Application.Services.organizationServices import *
from Domain.extension import api, authorizations
from Utils.Exceptions.customException import CustomException
from Infrastructure.Repositories.organizationXadminRepo import postorganizationXadminRepository
from Infrastructure.Repositories.OrganizationAdminRepo import createNewOrganizationAdminRepo,deleteOrganizationAdminRoleRepo

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
            organizationXadmin = dict()

            organization = postOrganizationService(organization)

            api.payload["organizationId"] = organization["id"]
            api.payload.pop("url")
            api.payload.pop("adress")
            api.payload.pop("organizationName")

            token,organizationXadmin["employeeId"] = postUserService(api.payload)
            organizationXadmin["organizationId"] = organization["id"]

            # TODO: check why organizationXadmin is not being used
            organizationXadmin=postorganizationXadminRepository(organizationXadmin)

            return {"Token": token}, 200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsAdmin.route("/delete/<string:email>")
class DeleteUser(Resource):
    method_decorators = [jwt_required()]

    @nsAdmin.doc(security="jsonWebToken")
    @nsAdmin.doc(params={"email": "User email"})

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

@nsAdmin.route("/customrole")
class PostRole(Resource):
    @nsAdmin.expect(teamRolePostExpect)
    def post(self):
        try:

            insertedRole = postCustomRoleService(api.payload)

            return insertedRole

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsAdmin.route("/promoteadmin/<string:employeeId>/<string:organizationId>")
class PromoteAdmin(Resource):
    def put(self,employeeId,organizationId):
        try:

            createNewOrganizationAdminRepo(employeeId,organizationId)

            return {"message":"Employee promoted succesfully"}

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")




@nsAdmin.route("/demoteorganizationadmin/<string:employeeId>")
class DemoteOrganizationAdmin(Resource):
    def delete(self, employeeId):
        try:

            deleteOrganizationAdminRoleRepo(employeeId)

            return {"message": "Demoted user succesfully"}

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")



