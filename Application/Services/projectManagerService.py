from Infrastructure.Repositories.ProjectManagerRepo import *
from Application.Services.userServices import getUserByIdService
def postProjectManagerService(id):

    getUserByIdService(id)

    postProjectManagerRepo(id)