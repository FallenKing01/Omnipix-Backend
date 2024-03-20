from Domain.extension import assignedSkillCollection,skillCollection,technologyStackCollection,customTeamRoleCollection,dealocationProposalCollection,skillXprojectCollection,projectCollection,projectManagerCollection,assignementProposalCollection,projectStatusCollection,employeesCollection,projectXemployeeCollection
from Infrastructure.Repositories.ProjectManagerRepo import updateProjectsOfManager
from datetime import datetime
from Utils.Exceptions.customException import CustomException

def postProjectRepo(project):

    insertedItm = projectCollection.document()
    insertedItmId = insertedItm.id

    updateProjects = {
        "employeeId":project["employeeId"],
        "projectId":insertedItmId
    }

    data = []
    data.append("xBAS2AnvKQlsO5JptESp")
    projectStatus = {
        "projectId": insertedItmId,
        "status":project["status"],
        "canDelete": True,
    }

    projectXemployeeToInsert = {
        "employeeId":project["employeeId"],
        "projectId":insertedItmId,
        "isActive":True,
        "organizationId":project["organizationId"],
        "numberOfHours":0,
        "teamRolesId":data
    }

    insertProjXemployee = projectXemployeeCollection.document()
    insertProjXemployeeId = insertProjXemployee.id
    projectXemployeeToInsert["id"] = insertProjXemployeeId

    projectXemployeeCollection.add(projectXemployeeToInsert)


    project.pop("status")
    updateProjectsOfManager(updateProjects)

    project["id"] = insertedItmId

    projectStatusCollection.add(projectStatus)
    projectCollection.add(project)

    return project

def updateProjectRepo(project):

    query = projectCollection.where("id", "==", project["projectId"])
    docs = query.get()

    # technologyToDelete = project.get("technologyToDelete", [])
    # technologyToAdd = project.get("technologyToAdd", [])
    # teamRolesToAdd = project.get("teamRolesToAdd", [])
    # teamRolesToDelete = project.get("teamRolesToDelete", [])
    #check conflict
    for doc in docs:
        doc.reference.update({
            "technologyStack": project["technologyStack"],
            "teamRoles": project["teamRoles"],
            "name": project["name"],
            "period": project["period"],
            "startDate": project["startDate"],
            "description": project["description"],
        })
    query = projectStatusCollection.where("projectId", "==", project["projectId"]).get()
    for doc in query:
        if project["status"] == "In Progress" or project["status"] == "Closed" or project["status"] == "Closing":
            project["canDelete"] = False

        doc.reference.update({
            "status": project["status"] ,
            "canDelete": project["canDelete"]
        })

        # current_technology_stack = doc.to_dict().get("technologyStack", [])
        #
        # for tech in technologyToDelete:
        #     if tech in current_technology_stack:
        #         current_technology_stack.remove(tech)
        #
        # for tech in technologyToAdd:
        #     current_technology_stack.append(tech)
        #
        # doc.reference.update({
        #     "technologyStack": current_technology_stack
        # })
        #
        # current_team_roles = doc.to_dict().get("teamRoles", {})
        #
        # for role_id in teamRolesToDelete:
        #     if role_id in current_team_roles:
        #         del current_team_roles[role_id]
        #
        # current_team_roles.update(teamRolesToAdd)
        #
        # doc.reference.update({
        #     "teamRoles": current_team_roles
        # })

def getProjectByIdRepo(id):
    query = projectCollection.where("id","==",id).get()

    project = None

    for doc in query:
        project = doc.to_dict()

    return project

def getEmployeesPartiallyAvailable(id):

    query = employeesCollection.where("organizationId", "==", id).order_by("workingHours").get()

    employeeSorted = []

    for doc in query:
        employee_data = doc.to_dict()
        employeeSorted.append(employee_data)

    return employeeSorted

def assignProposalRepo(assignRequest):
    insertedItm = assignementProposalCollection.document()
    insertedItmId= insertedItm.id

    assignRequest["id"] = insertedItmId

    query = employeesCollection.where("id","==",assignRequest["employeeId"]).get()
    for doc in query:
        currentDoc = doc.to_dict()
        currentDoc.pop("password",None)
        assignRequest["departamentId"] = currentDoc["departamentId"]

    assignementProposalCollection.add(assignRequest)

    return assignRequest


def getAssignmentProjectRequestRepo(id):
    query = assignementProposalCollection.where("departamentId", "==", id).get()

    assignments = []

    for doc in query:
        currentDoc = doc.to_dict()
        assignments.append(currentDoc)

    return assignments

def closeProjectRepo(id):

    query = projectXemployeeCollection.where("projectId","==",id).get()

    for doc in query:
        doc.reference.update({"isActive":False})

    query = projectStatusCollection.where("projectId","==",id).get()

    for doc in query:
        doc.reference.update({"status" : "Closed"})

def getPastProjectMembersRepo(projectId):

    query = projectXemployeeCollection.where("projectId","==",projectId).where("isActive","==",False).get()

    employeeIds= []

    for doc in query:
        currentDoc = doc.to_dict()
        employeeIds.append(currentDoc["employeeId"])

    if not employeeIds:
        raise CustomException(404,"No employees")

    employeesQuery = employeesCollection.where("id", "in", employeeIds).get()

    employeeData = []

    for doc in employeesQuery:
        currentDoc = doc.to_dict()
        currentDoc.pop('password', None)
        teamRoleIdQuery = projectXemployeeCollection.where("projectId","==",projectId).where("employeeId","==",currentDoc["id"]).get()
        teamRoleIds = []
        for docId in teamRoleIdQuery:
            currentTeamRoleId = docId.to_dict()
            teamRoleIds=currentTeamRoleId["teamRolesId"]
        teamRoleData = []
        if teamRoleIds:
            teamRoleQuery = customTeamRoleCollection.where("id","in",teamRoleIds).get()

            for teamRoleName in teamRoleQuery:
                currentTeamRole = teamRoleName.to_dict()
                teamRoleData.append(currentTeamRole)

        currentDoc["teamRolesId"] = teamRoleData
        employeeData.append(currentDoc)


    return employeeData

def getCurrentProjectMembersRepo(projectId):

    query = projectXemployeeCollection.where("projectId","==",projectId).where("isActive","==",True).get()

    employeeIds= []

    for doc in query:
        currentDoc = doc.to_dict()
        currentDoc.pop('password', None)
        employeeIds.append(currentDoc["employeeId"])

    if not employeeIds:
        raise CustomException(404,"No employees")

    employeesQuery = employeesCollection.where("id", "in", employeeIds).get()

    employeeData = []

    for doc in employeesQuery:
        currentDoc = doc.to_dict()
        currentDoc.pop('password', None)


        queryRoles = projectXemployeeCollection.where("projectId","==",projectId).where("employeeId","==",currentDoc["id"]).get()

        for docRoles in queryRoles:
            currentDocRoles = docRoles.to_dict()
            ownedRolesId=currentDocRoles["teamRolesId"]
        dataRoles = []

        if ownedRolesId:
            queryRoles = customTeamRoleCollection.where("id","in",ownedRolesId).get()
            for roleName in queryRoles:
                currentRole = roleName.to_dict()
                dataRoles.append(currentRole)

        currentDoc["teamRolesId"] = dataRoles

        employeeData.append(currentDoc)

    return employeeData

def getInfoPastProjectsRepo(employeeId):
    query = projectXemployeeCollection.where("isActive", "==", False).where("employeeId", "==", employeeId).get()

    projectIds = []

    for doc in query:
        currentDoc = doc.to_dict()
        projectIds.append(currentDoc["projectId"])

    if not projectIds:
        raise CustomException(404, "No projects")

    projectQuery = projectCollection.where("id", "in", projectIds).get()

    projectData = {}  # Initialize projectData as a dictionary

    for doc in projectQuery:
        currentDoc = doc.to_dict()

        getStatusOfProject = projectStatusCollection.where("projectId", "==", currentDoc["id"]).get()
        for docStatus in getStatusOfProject:
            currentDoc["status"] = docStatus.to_dict()["status"]

        if "teamRoles" in currentDoc:
            teamRolesFinal = []
            teamRolesIds = []
            teamRolesValues = []

            for key, value in currentDoc["teamRoles"].items():
                teamRolesIds.append(key)
                teamRolesValues.append(value)

            teamRoleQuery = customTeamRoleCollection.where("id", "in", teamRolesIds).get()

            for doc, value in zip(teamRoleQuery, teamRolesValues):
                currentDocRoles = doc.to_dict()
                currentDocRoles["value"] = value
                teamRolesFinal.append(currentDocRoles)

            currentDoc["teamRoles"] = teamRolesFinal

        if "technologyStack" in currentDoc:
            technologyStackFinal = []
            technologyStackIds = []

            for key in currentDoc["technologyStack"]:
                technologyStackIds.append(key)

            techStackQuery = technologyStackCollection.where("id", "in", technologyStackIds).get()

            for doc in techStackQuery:
                currentDocTech = doc.to_dict()
                technologyStackFinal.append(currentDocTech)

            currentDoc["technologyStack"] = technologyStackFinal

        projectData[currentDoc["id"]] = currentDoc

    return list(projectData.values())


def getInfoCurrentProjectsRepo(employeeId):
    query = projectXemployeeCollection.where("isActive", "==", True).where("employeeId", "==", employeeId).get()

    projectIds = []

    for doc in query:
        currentDoc = doc.to_dict()
        projectIds.append(currentDoc["projectId"])

    if not projectIds:
        raise CustomException(404, "No projects")

    projectQuery = projectCollection.where("id", "in", projectIds).get()

    projectData = {}  # Initialize projectData as a dictionary

    for doc in projectQuery:
        currentDoc = doc.to_dict()

        getStatusOfProject = projectStatusCollection.where("projectId", "==", currentDoc["id"]).get()

        for docStatus in getStatusOfProject:
            currentDoc["status"] = docStatus.to_dict()["status"]

        teamRolesFinal = []
        technologyStackIds =[]
        technologyStackFinal = []
        teamRolesIds = []
        teamRolesValues = []

        for key, value in currentDoc["teamRoles"].items():
            teamRolesIds.append(key)
            teamRolesValues.append(value)
        for key in currentDoc["technologyStack"]:
            technologyStackIds.append(key)
        if teamRolesIds:
            teamRoleQuery = customTeamRoleCollection.where("id", "in", teamRolesIds).get()

            for doc, value in zip(teamRoleQuery, teamRolesValues):
                currentDocRoles = doc.to_dict()
                currentDocRoles["value"] = value
                teamRolesFinal.append(currentDocRoles)

            currentDoc["teamRoles"] = teamRolesFinal

        if technologyStackIds:
            techStackQuery = technologyStackCollection.where("id", "in", technologyStackIds).get()
            for doc in techStackQuery:
                currentDocTech = doc.to_dict()
                technologyStackFinal.append(currentDocTech)
            currentDoc["technologyStack"] = technologyStackFinal
        projectData[currentDoc["id"]] = currentDoc

    return list(projectData.values())

def getProjectsFromOrganizationRepo(organizationId):
    query = projectCollection.where("organizationId", "==", organizationId).get()

    finalProjects = []

    for doc in query:
        project = doc.to_dict()

        teamRolesIds = []
        teamRolesValues = []

        for key, value in project["teamRoles"].items():
            teamRolesIds.append(key)
            teamRolesValues.append(value)

        if teamRolesIds:
            queryRoles = customTeamRoleCollection.where("id", "in", teamRolesIds).get()
            toInsertRoles = []

            for docRoles, value in zip(queryRoles, teamRolesValues):
                currentDoc = docRoles.to_dict()
                currentDoc["value"] = value
                toInsertRoles.append(currentDoc)

            project["teamRoles"] = toInsertRoles

        technologyStackId = []

        for valueTec in project["technologyStack"]:
            technologyStackId.append(valueTec)

        if technologyStackId:
            queryTech = technologyStackCollection.where("id", "in", technologyStackId).get()
            technologyStackToReturn = []

            for docTechnology in queryTech:
                technologyStackToReturn.append(docTechnology.to_dict())

            project["technologyStack"] = technologyStackToReturn

        finalProjects.append(project)

    if not finalProjects:
        raise CustomException(404, "No projects")

    return finalProjects


def getProjectsForDepartamentManagerEmployeeRepo(departmentId):
    queryEmployee = employeesCollection.where("departamentId", "==", departmentId).get()
    employeeIds = []
    print(queryEmployee)
    for doc in queryEmployee:
        currentDoc = doc.to_dict()
        currentDoc.pop('password', None)
        employeeIds.append(currentDoc["id"])

    if not employeeIds:
        raise CustomException(404, "Employees not found in department")

    projectIds = []
    queryProjectEmployee = projectXemployeeCollection.where("employeeId", "in", employeeIds).get()

    for doc in queryProjectEmployee:
        currentDoc = doc.to_dict()
        projectIds.append(currentDoc["projectId"])

    if not projectIds:
        raise CustomException(404, "Projects not found for members of your department")

    projectsData = []
    queryProject = projectCollection.where("id", "in", projectIds).get()

    for doc in queryProject:
        projectData = doc.to_dict()

        # Fetch complete technology objects
        technologyIds = projectData.get("technologyStack", [])
        technologyData = []
        if technologyIds:
            technologyQuery = technologyStackCollection.where("id", "in", technologyIds).get()
            for techDoc in technologyQuery:
                technologyData.append(techDoc.to_dict())
            projectData["technologyStack"] = technologyData

        statusQuery = projectStatusCollection.where("projectId", "==", projectData["id"]).get()
        for statusDoc in statusQuery:
            currentStatus = statusDoc.to_dict()
            projectData["status"] = currentStatus["status"]

        teamRolesToAppend = []
        teamRoles = projectData.get("teamRoles", {})
        if teamRoles:
            for roleId, roleValue in teamRoles.items():
                roleDoc = customTeamRoleCollection.document(roleId).get()
                if roleDoc.exists:
                    roleData = roleDoc.to_dict()
                    roleData["value"] = roleValue
                    teamRolesToAppend.append(roleData)

            projectData["teamRoles"] = teamRolesToAppend

        projectsData.append(projectData)

    if not projectsData:
        raise CustomException(404, "No projects found for department")

    return projectsData



def getProjectDetailsRepo(projectId):

    query = projectCollection.where("id","==",projectId).get()

    project = None

    for doc in query:
        project = doc.to_dict()

    if project is None:
        raise CustomException(404,"There is no project with this id")

    teamRolesIds = []
    teamRolesValues = []

    for key, value in project["teamRoles"].items():
        teamRolesIds.append(key)
        teamRolesValues.append(value)

    if teamRolesIds:
        query = customTeamRoleCollection.where("id","in",teamRolesIds).get()
        toInsertRoles = []

        for doc, value in zip(query, teamRolesValues):
            currentDoc = doc.to_dict()
            # Adding the value from teamRolesValues to currentDoc
            currentDoc["value"] = value
            toInsertRoles.append(currentDoc)
        project["teamRoles"] = toInsertRoles

    technologyStackId = []
    technologyStackToReturn = []

    for value in project["technologyStack"]:
        technologyStackId.append(value)
    print(technologyStackId)

    if technologyStackId:
        query = technologyStackCollection.where("id","in",technologyStackId).get()

        for doc in query:
            currentDoc = doc.to_dict()
            technologyStackToReturn.append(currentDoc)

        project["technologyStack"] = technologyStackToReturn

    return project


def projectToDeleteRepo(projectId):
        query = projectCollection.where("id", "==", projectId).get()
        for doc in query:
            doc.reference.delete()

        query = projectManagerCollection.where("projectId", "==", projectId).get()
        for doc in query:
            doc.reference.delete()

        query = projectStatusCollection.where("projectId", "==" ,projectId).get()
        for doc in query:
            doc.reference.delete()

        query = skillXprojectCollection.where("projectId","==",projectId).get()

        for doc in query:
            doc.reference.delete()

        query = projectXemployeeCollection.where("projectId","==",projectId).get()


        for doc in query:
            doc.reference.delete()

        query = assignementProposalCollection.where("projectId","==",projectId).get()

        for doc in query:
            doc.reference.delete()

        query = dealocationProposalCollection.where("projectId","==",projectId).get()

        for doc in query:
            doc.reference.delete()

def getProjectAfterStatusRepo(status,organizationId):
    query = projectCollection.where("organizationId","==",organizationId).get()

    projectIds = []
    for doc in query:
        currentDoc = doc.to_dict()
        projectIds.append(currentDoc["id"])

    projectResult = []

    if projectIds:
        query = projectStatusCollection.where("status","==",status).where("projectId","in",projectIds).get()

        for doc in query:
            currentDoc = doc.to_dict()
            currentDoc.pop("creationDate")
            projectResult.append(currentDoc)

    return projectResult

def getProposedMembersRepo(projectId):
    query = assignementProposalCollection.where("projectId","==",projectId).get()

    proposedMembers = []

    if query:
        for doc in query:
            currentDoc = doc.to_dict()

            queryEmployee =employeesCollection.where("id","==",currentDoc["employeeId"]).get()

            if queryEmployee:
                for docEmployee in queryEmployee:
                    currentEmployee = docEmployee.to_dict()
                    currentEmployee.pop("password",None)
                    currentDoc["employeeId"] = currentEmployee
                proposedMembers.append(currentDoc)

    return proposedMembers


def partiallyAvailableEmployeesRepo(organizationId, projectId):
    query = employeesCollection.where("organizationId", "==", organizationId).get()
    projectQuery = projectCollection.where("id", "==", projectId).get()
    projectSkillsRequired = []
    projectSkills = []
    technologyStackNames = []

    for doc in projectQuery:
        currentDoc = doc.to_dict()
        projectSkills = currentDoc["technologyStack"]

    projectSkillsRequired = technologyStackCollection.where("id", "in", projectSkills).get()

    for doc in projectSkillsRequired:
        currentDoc = doc.to_dict()
        technologyStackNames.append(currentDoc["name"])

    finalResult = []

    if query:
        for doc in query:
            currentDoc = doc.to_dict()
            if currentDoc["departamentId"] != None:
                if currentDoc["workingHours"] < 8 and currentDoc["workingHours"] > 0:
                    currentDoc.pop("password", None)
                    skillName = []
                    assignedSkills = assignedSkillCollection.where("employeeId", "==", currentDoc["id"]).get()
                    skillsIds = []

                    for skills in assignedSkills:
                        currentSkill = skills.to_dict()
                        skillsIds.append(currentSkill["skillId"])

                    currentEmployeeSkills = skillCollection.where("id", "in", skillsIds).get()
                    for skill in currentEmployeeSkills:
                        currentSkill = skill.to_dict()
                        skillName.append(currentSkill["name"])

                    for skill in skillName:
                        for tech_stack in technologyStackNames:
                            if tech_stack.lower() in skill.lower() or skill.lower() in tech_stack.lower():
                                finalResult.append(currentDoc)

    return finalResult

def unavibleEmployeesRepo(organizationId, projectId):
    query = employeesCollection.where("organizationId", "==", organizationId).get()
    projectQuery = projectCollection.where("id", "==", projectId).get()
    projectSkillsRequired = []
    projectSkills = []
    technologyStackNames = []

    for doc in projectQuery:
        currentDoc = doc.to_dict()
        projectSkills = currentDoc["technologyStack"]

    projectSkillsRequired = technologyStackCollection.where("id", "in", projectSkills).get()

    for doc in projectSkillsRequired:
        currentDoc = doc.to_dict()
        technologyStackNames.append(currentDoc["name"])

    finalResult = []

    if query:
        for doc in query:
            currentDoc = doc.to_dict()
            if currentDoc["departamentId"] != None:
                if currentDoc["workingHours"] ==8:
                    currentDoc.pop("password", None)
                    skillName = []
                    assignedSkills = assignedSkillCollection.where("employeeId", "==", currentDoc["id"]).get()
                    skillsIds = []

                    for skills in assignedSkills:
                        currentSkill = skills.to_dict()
                        skillsIds.append(currentSkill["skillId"])

                    currentEmployeeSkills = skillCollection.where("id", "in", skillsIds).get()
                    for skill in currentEmployeeSkills:
                        currentSkill = skill.to_dict()
                        skillName.append(currentSkill["name"])

                    for skill in skillName:
                        for tech_stack in technologyStackNames:
                            if tech_stack.lower() in skill.lower() or skill.lower() in tech_stack.lower():
                                finalResult.append(currentDoc)

    return finalResult

def freeEmployeesRepo(organizationId, projectId):
    query = employeesCollection.where("organizationId", "==", organizationId).get()
    projectQuery = projectCollection.where("id", "==", projectId).get()
    projectSkillsRequired = []
    projectSkills = []
    technologyStackNames = []

    for doc in projectQuery:
        currentDoc = doc.to_dict()
        projectSkills = currentDoc["technologyStack"]

    projectSkillsRequired = technologyStackCollection.where("id", "in", projectSkills).get()

    for doc in projectSkillsRequired:
        currentDoc = doc.to_dict()
        technologyStackNames.append(currentDoc["name"])

    finalResult = []

    if query:
        for doc in query:
            currentDoc = doc.to_dict()
            if currentDoc["departamentId"] != None:

                if currentDoc["workingHours"] == 0:
                    currentDoc.pop("password", None)
                    skillName = []
                    assignedSkills = assignedSkillCollection.where("employeeId", "==", currentDoc["id"]).get()
                    skillsIds = []

                    for skills in assignedSkills:
                        currentSkill = skills.to_dict()
                        skillsIds.append(currentSkill["skillId"])

                    if skillsIds:  # Check if skillsIds is not empty before executing the query
                        currentEmployeeSkills = skillCollection.where("id", "in", skillsIds).get()
                        for skill in currentEmployeeSkills:
                            currentSkill = skill.to_dict()
                            skillName.append(currentSkill["name"])

                    for skill in skillName:
                        for tech_stack in technologyStackNames:
                            if tech_stack.lower() in skill.lower() or skill.lower() in tech_stack.lower():
                                finalResult.append(currentDoc)

    return finalResult

def projectCanBeDeletedRepo(projectId):
    query = projectStatusCollection.where("projectId", "==", projectId).get()

    for doc in query:
        currentDoc = doc.to_dict()
        if currentDoc["canDelete"] == False:
            return False#nu poate fi sters

    return True#poate fi sters



