from datetime import datetime, timedelta

import bcrypt
from flask_jwt_extended import create_access_token
from Infrastructure.Repositories.UserRepo import getUserByEmailRepository
from Utils.Exceptions.customException import CustomException


def loginService(account):
    user = getUserByEmailRepository(account["email"])

    if user is None:
        raise CustomException(404, "Account does not exist")

    # Ensure both passwords are encoded as bytes
    password_bytes = account["password"].encode('utf-8')

    # Check if the stored password is already bytes, if not, encode it
    stored_password = user["password"]
    if isinstance(stored_password, str):
        stored_password_bytes = stored_password.encode('utf-8')
    else:
        stored_password_bytes = stored_password

    if not bcrypt.checkpw(password_bytes, stored_password_bytes):
        raise CustomException(400, "Password is wrong")

    userData = {
        "id": user["id"],
        "name": user["name"],
        "workingHours": user["workingHours"],
        "email": user["email"],
        "organizationId": user["organizationId"],
        "departamentId": user["departamentId"]
    }

    expires = datetime.utcnow() + timedelta(days=30)

    token = create_access_token(
        userData,
        additional_claims=userData,
        expires_delta=expires - datetime.utcnow(),
    )

    return token




