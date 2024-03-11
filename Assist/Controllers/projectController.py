from Application.Dtos.expect.projectExpect import *
from flask_restx import Namespace, Resource
from flask import abort
from Domain.extension import  authorizations,api
from Utils.Exceptions.customException import CustomException
from Application.Services.projectService import postProjectService
nsProject = Namespace("project",authorizations=authorizations,description="Project operations")

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
