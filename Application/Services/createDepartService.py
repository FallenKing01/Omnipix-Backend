
from Infrastructure.Repositories.postManagerDepart import createDepartManRepo
from Application.Services.userServices import getUserByIdService
def postDepartManService(employee):
    getUserByIdService(employee["employeeId"])

    createDepartManRepo(employee)

    return employee
