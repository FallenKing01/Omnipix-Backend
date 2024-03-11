from flask_restx import Namespace, Resource
from flask import abort
from Domain.extension import  authorizations,api
from Application.Services.projectManagerService import *
from Utils.Exceptions.customException import CustomException
from Application.Services.tecnologyStackService import createTecnologyStackService
from Application.Dtos.expect.projectManagerExpect import technologyStackExpect
nsProjectManager = Namespace("projectmanager",authorizations=authorizations,description="Project manager operations")

@nsProjectManager.route("/createprojectmanager/<string:id>")
class PostProjectManager(Resource):
    def post(self,id):
        try:

            postProjectManagerService(id)


            return {"Message": "User was promoted to project manager"}, 200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsProjectManager.route("/technologystack")
class PostTechnologyStack(Resource):
    @nsProjectManager.expect(technologyStackExpect)
    def post(self):
        try:

            response = createTecnologyStackService(api.payload)

            return response

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")
