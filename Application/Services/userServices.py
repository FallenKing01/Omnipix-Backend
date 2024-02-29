from Infrastructure.Repositories.UserRepo import *

from Utils.Exceptions.customException import CustomException
from Domain.extension import salt
import bcrypt

def postUserService(user):

    existingUser = getUserByEmailRepository(user["email"])

    if existingUser is not None:
        raise CustomException(409, "The user with this email already exists")

    # Encode the password as bytes before hashing
    password_bytes = user["password"].encode('utf-8')
    user["password"] = bcrypt.hashpw(password_bytes, salt)

    token = postUserRepository(user)

    return token


def deleteUserService(email):

    existingUser = getUserByEmailRepository(email)

    if existingUser is None:
        raise CustomException(404,"User with this email does not exist")

    if len(email) < 5:
        raise CustomException(400,"Email is too short")

    deleteUserByEmailRepository(email)

def updatePasswordService(email,newPassword):

    existingUser = getUserByEmailRepository(email)

    if existingUser is None:
        raise CustomException(404,"User with this email does not exist")

    if len(email) < 5:
        raise CustomException(400,"Email is too short")

    updatePasswordRepository(email,newPassword)


