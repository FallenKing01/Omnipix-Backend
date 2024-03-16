from flask_restx import Namespace, Resource
from flask import abort
from Domain.extension import  authorizations,api
from Utils.Exceptions.customException import CustomException
from Application.Services.tecnologyStackService import createTecnologyStackService
from Application.Services.projectManagerService import *
from Application.Dtos.expect.projectManagerExpect import *
nsProjectManager = Namespace("projectmanager",authorizations=authorizations,description="Project manager operations")

@nsProjectManager.route("/searchname/<string:organizationId>/<string:name>")
class SearchNameUser(Resource):
    def get(self,organizationId,name):
        try:
            employee = {
                "organizationId":organizationId,
                "name":name,
            }

            response = searchUserService(employee)

            return response

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

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


@nsProjectManager.route("/demoteprojectmanager/<string:employeeId>")
class DemoteProjectManager(Resource):
    def delete(self,employeeId):
        try:

            deleteProjectManagerRepo(employeeId)

            return {"message":"Demoted user from project manager succesfully"}

        except CustomException as ce:
            abort(ce.statusCode, ce.message)
        except Exception:
            abort(500, "Something went wrong")

@nsProjectManager.route("/postskillcategory")
class PostSkillCategory(Resource):
    @nsProjectManager.expect(postSkillCategory)
    def post(self):
        try:

            return postCategory(api.payload)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)
        except Exception:
            abort(500, "Something went wrong")

@nsProjectManager.route("/getskillcategories/<string:organizationId>")
class GetSkillCategories(Resource):
    def get(self,organizationId):
        try:

            return getSkillCategoriesRepo(organizationId)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)
        except Exception:
            abort(500, "Something went wrong")

@nsProjectManager.route("/deletecategory/<string:categoryId>")
class DeleteCategory(Resource):
    def delete(self,categoryId):
        try:

            deleteCategoryRepo(categoryId)

            return {"message":"Category deleted succesfully"}

        except CustomException as ce:
            abort(ce.statusCode, ce.message)
        except Exception:
            abort(500, "Something went wrong")

