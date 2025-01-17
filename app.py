from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from Assist.Controllers.adminController import nsAdmin
from Assist.Controllers.loginController import nsLogin
from Assist.Controllers.employeeController import nsEmployee
from Assist.Controllers.organizationController import nsOrganization
from Assist.Controllers.departamentController import nsDepartament
from Assist.Controllers.departamentManagerController import nsDepartamentManager
from Assist.Controllers.projectManagerController import nsProjectManager
from Assist.Controllers.promoteDepartController import nsTest
from Assist.Controllers.projectController import nsProject
from Assist.Controllers.openaiController import nsOpenAi
from Assist.Controllers.notificationsController import nsNotifications
from Domain.extension import api

from Infrastructure.Repositories.UserRepo import getUserByIdRepository

app = Flask(__name__)

CORS(app)

app.config["JWT_SECRET_KEY"] = "cookiemonster"  # TODO: migrate to .env

api.init_app(app)

api.add_namespace(nsAdmin)
api.add_namespace(nsEmployee)
api.add_namespace(nsLogin)
api.add_namespace(nsOrganization)
api.add_namespace(nsDepartament)
api.add_namespace(nsDepartamentManager)
api.add_namespace(nsProjectManager)
api.add_namespace(nsTest)
api.add_namespace(nsProject)
api.add_namespace(nsOpenAi)
api.add_namespace(nsNotifications)

jwt = JWTManager(app)


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user["id"]


# JWT User Lookup Callback
@jwt.user_lookup_loader
def user_lookup_callback(jwt_header, jwt_data):
    identity = jwt_data["sub"]

    user = getUserByIdRepository(identity)
    return user


if __name__ == "__main__":

    app.run(debug=True)
