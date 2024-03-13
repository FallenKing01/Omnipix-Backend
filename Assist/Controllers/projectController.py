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

@nsProject.route("/assignproposal")
class CreateAssignmentProposal(Resource):
    @nsProject.expect(assignmentProposalExpect)
    def post(self):
        try:

            assignment = assignProposalService(api.payload)

            return assignment

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsProject.route("/assgnmentrequest/<string:departamentId>")
class GetAssignRequest(Resource):
    def get(self,departamentId):
        try:

            return getAssignmentProjectRequestService(departamentId)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsProject.route("/closeproject/<string:id>")
class CloseProject(Resource):
    def put(self,id):
        try:

            closeProjectService(id)

            return {"message":"You closed a project!"}

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsProject.route("/inactivemembersproject/<string:projectId>")
class GetInactiveMembersFromProject(Resource):
    def get(self,projectId):
        try:

            return getPastProjectMembersRepo(projectId)



        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsProject.route("/activemembersproject/<string:projectId>")
class GetActiveMembersFromProject(Resource):
    def get(self,projectId):
        try:

            return getCurrentProjectMembersRepo(projectId)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsProject.route("/projectdetailinactive/<string:employeeId>")
class GetInactiveUserInfoFromProject(Resource):
    def get(self,employeeId):
        try:

            return getInfoPastProjectsRepo(employeeId)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsProject.route("/projectdetailactive/<string:employeeId>")
class GetActiveUserInfoFromProject(Resource):
    def get(self,employeeId):
        try:

            return getInfoCurrentProjectsRepo(employeeId)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsProject.route("/getprojectsfromorganization/<string:organizationId>")
class GetProjectsFromOrganization(Resource):
    def get(self,organizationId):
        try:

            return getProjectsFromOrganizationRepo(organizationId)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsProject.route("/getprojectsfromadepartamentmembers/<string:departamentId>")
class GetProjectsFromOrganization(Resource):
    def get(self,departamentId):
        try:

            return getProjectsForDepartamentManagerEmployeeRepo(departamentId)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsProject.route("/getprojectdetail/<string:projectId>")
class GetProjectDetail(Resource):
    def get(self,projectId):
        try:

            return getProjectDetailsRepo(projectId)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsProject.route("/deleteproject/<string:projectId>")
class DeleteProject(Resource):
    def delete(self,projectId):
        try:
            projectToDeleteRepo(projectId)
            return {"message":"Project deleted"}

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")