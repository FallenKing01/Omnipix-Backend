from flask import abort
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from Application.Dtos.expect.organizationExpect import organizationPostExpect


from Application.Services.organizationServices import postOrganizationService
from Domain.extension import api,authorizations
from Utils.Exceptions.customException import CustomException

nsOrganization = Namespace("organization", authorizations=authorizations , description="Organizations operations")


@nsOrganization.route("/create")
class PostOrganization(Resource):
    @nsOrganization.expect(organizationPostExpect)

    def post(self):
        try:
            return postOrganizationService(api.payload)
        except CustomException as ce:
            abort(ce.statusCode, ce.message)
        except Exception as e:
            abort(500, "Something went wrong")