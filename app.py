from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from Domain.extension import api
from Assist.Controllers.userController import nsUser
from Assist.Controllers.loginController import nsLogin
from Infrastructure.Repositories.UserRepo import getUserByIdRepository
from Assist.Controllers.organizationController import nsOrganization
app = Flask(__name__)

CORS(app)

app.config["JWT_SECRET_KEY"] = "cookiemonster"



api.init_app(app)
api.add_namespace(nsUser)
api.add_namespace(nsLogin)
api.add_namespace(nsOrganization)
#mongo = PyMongo(app)
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
