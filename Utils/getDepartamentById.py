from Domain.extension import departamentCollection
from http import HTTPStatus
from Utils.Exceptions.customException import CustomException
from Infrastructure.Repositories.DepartamentRepo import getDepartamentManagerByEmployeeIdRepo

def getDepartmentByIdRepo(id):
    query = departamentCollection.where("id", "==", id).limit(1).get()
    department = None

    for doc in query:
        department = doc.to_dict()
        break

    return department


def getDepartamentManagerByEmployeeIdService(id):

    isManager = getDepartamentManagerByEmployeeIdRepo(id)

    if isManager is None:
        raise CustomException(HTTPStatus.NOT_FOUND, "The employee is not departament manager!")

    return isManager
