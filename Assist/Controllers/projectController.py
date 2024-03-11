from Application.Dtos.expect.projectExpect import *
from flask_restx import Namespace, Resource
from flask import abort
from Domain.extension import  authorizations,api
from Utils.Exceptions.customException import CustomException
from Application.Services.projectService import postProjectService
nsProject = Namespace("project",authorizations=authorizations,description="Project operations")
from Application.Services.projectService import *
@nsProject.route("")
class CreateProject(Resource):
    @nsProject.expect(postProjectExpect)
    def post(self):
        try:

            project = postProjectService(api.payload)

            return project

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")
@nsProject.route("/updateproject")
class UpdateProject(Resource):
    @nsProject.expect(updateProjectExpect)
    def put(self):

        try:

            project = updateProjectService(api.payload)

            return project

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")