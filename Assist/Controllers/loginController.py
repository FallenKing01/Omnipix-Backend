
from flask import abort
from flask_restx import Namespace, Resource

from Application.Dtos.expect.loginExpect import loginExpect
from Application.Services.loginService import loginService
from Domain.extension import api
from Utils.Exceptions.customException import CustomException

nsLogin = Namespace("login", description="Login user")

@nsLogin.route("/")
class LoginApi(Resource):
    @nsLogin.expect(loginExpect)
    def post(self):
        try:
            token = loginService(api.payload)

            return {"Authentication successful" : token},201
        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception as e:
            abort(500, "Something went wrong")
