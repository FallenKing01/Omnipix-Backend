from datetime import datetime, timedelta

import bcrypt
from flask_jwt_extended import create_access_token
from Infrastructure.Repositories.UserRepo import getUserByEmailRepository
from Utils.Exceptions.customException import CustomException


def loginService(account):

    user = getUserByEmailRepository(account["email"])

    if user is None:
        raise CustomException(404,"Account does not exist")

    account["password"] = account["password"].encode('utf-8')

    if not bcrypt.checkpw(account["password"], user["password"]):
        raise CustomException(400, "Password is wrong")

    userData = {
        "id": user["id"],
        "name":user["name"],
        "workingHours":user["workingHours"],
        "email": user["email"],
        "organizationId":user["organizationId"],
        "departamentId":user["departamentId"]
    }

    expires = datetime.utcnow() + timedelta(days=30)

    token = create_access_token(
            userData,
            additional_claims=userData,
            expires_delta=expires - datetime.utcnow(),
        )

    return token


