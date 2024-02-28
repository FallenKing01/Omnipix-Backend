from flask import abort
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from Application.Dtos.expect.userExpect import userPostExpect
from Application.Dtos.post.userResponse import userPostResponse
from Application.Services.userServices import *
from Domain.extension import api,authorizations
from Utils.Exceptions.customException import CustomException

nsUser = Namespace("user", authorizations=authorizations , description="User operations")

@nsUser.route("/create")
class PostUser(Resource):

    @nsUser.expect(userPostExpect)
    @nsUser.marshal_with(userPostResponse)

    def post(self):
        try:
            user = postUserService(api.payload)
            return user, 200

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
            print(f"Unexpected exception: {e}")
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
            print(f"Unexpected exception: {e}")
            abort(500, "Something went wrong")






