import datetime

from Domain.extension import assignedSkillCollection, dealocationProposalCollection, projectXemployeeCollection, \
    assignementProposalCollection, departamentManagerCollection, departamentCollection, employeesCollection, \
    skillCollection

from Utils.Exceptions.customException import CustomException


def postDepartamentRepoADDITIONAL(depart):

    # IAU DOAR CE AM NEV PENTRU MANAGER
    managerDepartament = {
        "id": depart["departamentManagerId"],
        "employeeId": None,
        "departamentId": depart["departamentId"],
        "organizationId": depart["organizationId"]
    }

    departamentManagerCollection.add(managerDepartament)

    # RESTRUCTUREZ FORMA DEPARTAMENT SA ARATE CA IN TABELA
    depart["id"] = depart["departamentId"]
    depart.pop("departamentId")

    departamentCollection.add(depart)

    return depart

def postDepartamentRepo(depart):

    insertedItm = departamentCollection.document()
    insertedItmId = insertedItm.id

    depart["id"]= insertedItmId
    depart["departamentManagerId"] =None

    departamentCollection.add(depart)

    return depart


def postDepartamentWithManagerRepo(depart):

    # IAU DOAR CE AM NEV PENTRU MANAGER
    managerDepartament = {
        "id" : depart["departamentManagerId"],
        "employeeId" : depart["employeeId"],
        "departamentId": depart["departamentId"],
        "organizationId": depart["organizationId"]
    }

    departamentManagerCollection.add(managerDepartament)

    #RESTRUCTUREZ FORMA DEPARTAMENT SA ARATE CA IN TABELA
    depart.pop("employeeId")
    depart["id"] = depart["departamentId"]
    depart.pop("departamentId")

    departamentCollection.add(depart)

    return depart



def getDepartamentManagerByEmployeeIdRepo(id):

    query = departamentManagerCollection.where("employeeId", "==", id).limit(1).get()

    department = None

    for doc in query:
        department = doc.to_dict()
        break

    return department


def updateDepartamentManagerRepo(department):
    query = departamentManagerCollection.where("departamentId", "==", department["departamentId"]).limit(1).get()

    for doc in query:
        documentRef = doc.reference

        pastManager = doc.to_dict().get("employeeId")

        documentRef.update({"employeeId": department["employeeId"]})

        #actualizez departamentId pentru noul departamentManager
        employeeQuery = employeesCollection.where("id","==",department["employeeId"]).get()
        for updateEmployee in employeeQuery:
            employeeRef = updateEmployee.reference
            employeeRef.update({"departamentId" : department["departamentId"]})

        # actualizez departamentId pentru vechiul departamentManager in tabela employee
        pastManagerQuery = employeesCollection.where("id", "==", pastManager).get()
        for updatePastManager in pastManagerQuery:
            updatePastManager.reference.update({"departamentId": None})

        #actualizez skilurile
        skillQuery = skillCollection.where("currentManager", "==", pastManager).get()

        for updateSkills in skillQuery:
            skillsRef = updateSkills.reference
            skillsRef.update({"currentManager": department["employeeId"]})

    return query


def getDepartmentByIdRepo(id):
    """ Get department by id """
    for doc in departamentCollection.where("id", "==", id).limit(1).get():
        return doc.to_dict()


def updateSecondTimeManagerOfDepartamentRepo(user):
    print("User data:", user)

    # Update the employeeId in departamentManagerCollection
    query = departamentManagerCollection.where("departamentId", "==", user["departamentId"]).limit(1).get()
    print("Departament Manager Query Result:", query)

    for doc in query:
        print("Document Reference:", doc.reference)
        # Update the employeeId
        doc.reference.update({"employeeId": user["employeeId"]})

    # Update the departamentId in employeesCollection
    query = employeesCollection.where("id", "==", user["employeeId"]).get()
    print("Employees Query Result:", query)

    for doc in query:
        # Update the departamentId
        doc.reference.update({"departamentId": user["departamentId"]})



def updateNameOfDepartamentRepo(departament):

    query = departamentCollection.where("id", "==", departament["departamentId"]).limit(1).get()

    for doc in query:
        doc.reference.update({"name": departament["name"]})

def deleteDepartamentRepo(id):

    query = departamentCollection.where("id", "==", id).limit(1).get()

    for doc in query:
        doc.reference.delete()

    query = departamentManagerCollection.where("departamentId",'==',id).get()

    for doc in query:
        doc.reference.delete()

    query = employeesCollection.where("departamentId",'==',id).get()

    for doc in query:
        doc.reference.update({"departamentId": None})





def firstDepartamentManagerPromotionRepo(depart):

    query = departamentManagerCollection.where("employeeId", "==", depart["employeeId"]).limit(1).get()

    for doc in query:
        doc.reference.update({"departamentId": depart["departamentId"]})
        idChange = doc.get("id")
    query = departamentCollection.where("id","==",depart["departamentId"]).limit(1).get()

    for doc in query:
        doc.reference.update({"departamentManagerId": idChange})

    query = employeesCollection.where("id","==",depart["employeeId"]).limit(1).get()

    for doc in query:
        doc.reference.update({"departamentId":depart["departamentId"]})



def getDepartamentManagerWithNoDepartament(id):
    query = departamentManagerCollection.where('organizationId', '==', id).where("departamentId","==",None).get()
    employeeIds = []

    for doc in query:
        currentDoc = doc.to_dict()
        employeeIds.append(currentDoc["employeeId"])

    if not employeeIds:
        raise CustomException(404, "Are not managers with no departament in organization")

    query = employeesCollection.where("id","in",employeeIds).get()

    managers = []

    for doc in query:
        currentDoc = doc.to_dict()
        currentDoc.pop("password",None)
        managers.append(currentDoc)

    if not managers:
        raise CustomException(404,"Departament managers not found")

    return managers



def acceptProjectProposalRepo(project):

    insertedItm = projectXemployeeCollection.document()
    insertedItmId = insertedItm.id

    project["id"] = insertedItmId

    query = employeesCollection.where("id", "==", project["employeeId"]).limit(1).get()

    for doc in query:
        currentDoc = doc.to_dict()
        currentDoc.pop("password", None)

        totalWorkingHours = currentDoc.get("workingHours", 0) + project.get("workingHours", 0)

        if totalWorkingHours <= 8:
            employeesCollection.document(doc.id).update({"workingHours": totalWorkingHours})

            # Delete the proposal document from the collection
            proposal_query = assignementProposalCollection.where("id", "==", project["assignementProposalId"]).limit(1).get()
            for proposal_doc in proposal_query:
                proposal_doc.reference.delete()
        else:
            raise CustomException(409, "An employee can't work more than 8 hours a day")

        projectXemployeeCollection.add(project)
    return project

def declineProposalProjectRepo(id):

    query = assignementProposalCollection.where("id", "==", id).get()

    for doc in query:
        doc.reference.delete()


def dealocationProposalRepo(dealocation):

    insertedItm = dealocationProposalCollection.document()
    insertedItmId = insertedItm.id

    dealocation["id"] = insertedItmId

    dealocationProposalCollection.add(dealocation)

    return dealocation

def acceptDealocationProposalRepo(deallocation):
    projectEmployeeQuery = projectXemployeeCollection.where("projectId", "==", deallocation["projectId"]).where("employeeId", "==", deallocation["employeeId"]).get()

    for projectEmployeeDoc in projectEmployeeQuery:
        projectEmployeeDoc.reference.update({"isActive": False})

    employeeQuery = employeesCollection.where("id", "==", deallocation["employeeId"]).get()

    for employeeDoc in employeeQuery:
        employeeDocDict = employeeDoc.to_dict()
        employeeDocDict.pop("password", None)
        updatedWorkingHours = employeeDocDict["workingHours"] - projectEmployeeDoc.to_dict()["workingHours"]
        employeeDoc.reference.update({"workingHours": updatedWorkingHours})

    # Delete dealocation proposal
    dealocationQuery = dealocationProposalCollection.where("id", "==", deallocation["dealocatedId"]).get()

    for dealocationDoc in dealocationQuery:
        dealocationDoc.reference.delete()




def declineDealocationProposalRepo(id):

    query = dealocationProposalCollection.where("id","==",id).get()

    for doc in query:
        doc.reference.delete()


def getDepartamentAllocationProposalRepo(departamentId):
    for doc in assignementProposalCollection.where("departamentId", "==", departamentId).get():
        yield doc.to_dict()


def getDealocationProposalRepo(departamentId):
    query = dealocationProposalCollection.where("departamentId", "==", departamentId).get()

    dealocations = []

    for doc in query:
        currentDoc = doc.to_dict()
        dealocations.append(currentDoc)

    return dealocations

def getDepartamentsRepo(organizationId):
    # Querying departments
    query_departments = departamentCollection.where("organizationId", "==", organizationId).get()
    departaments = []

    departamentManagerId = []
    for doc in query_departments:
        current_doc = doc.to_dict()
        departaments.append(current_doc)
        if current_doc["departamentManagerId"] is not None:
            departamentManagerId.append(current_doc["departamentManagerId"])

    if not departamentManagerId:
        raise CustomException(404, "Departments not found")

    query_departament_manager = departamentManagerCollection.where("id", "in", departamentManagerId).get()
    employeesId = []

    for doc in query_departament_manager:
        current_doc = doc.to_dict()
        employeesId.append(current_doc["employeeId"])

    # Querying employee names
    query_employee = employeesCollection.where("id", "in", employeesId).get()
    managerNames = [doc.to_dict()["name"] for doc in query_employee]

    for i, doc in enumerate(managerNames):
        departaments[i]["managersName"] = doc

    # Counting members per department
    query_employee = employeesCollection.where("organizationId", "==", organizationId).get()
    count_members = {}
    for doc in query_employee:
        current_doc = doc.to_dict()
        department_id = current_doc.get("departamentId")  # Assuming this is the department ID field
        # Increment the count for the department
        count_members[department_id] = count_members.get(department_id, 0) + 1

    values = count_members.values()
    for department, value in zip(departaments, values):
        department["numberOfEmployees"] = value

    if not departaments:
        raise CustomException(404, "No departments")

    return departaments


def assignSkillDirectlyRepo(skill):
    # Assuming assignedSkillCollection is a Firestore collection reference
    insertedItm = assignedSkillCollection.document()
    insertedItmId = insertedItm.id

    # Adding necessary fields to the skill dictionary
    skill["id"] = insertedItmId
    skill["isApproved"] = True
    skill["dateTime"] = datetime.datetime.utcnow().isoformat()

    assignedSkillCollection.add(skill)

    return skill


def getChartSkillsRepo(departmentId, skillId):
    # Query employees in the specified department
    query_employee = employeesCollection.where("departamentId", "==", departmentId).stream()
    employees = [doc.id for doc in query_employee]

    # Check if employees exist in the department
    if not employees:
        raise CustomException(404, "No employees found in the department")

    # Query assigned skills for the retrieved employees and specified skillId
    query_skills = assignedSkillCollection.where("employeeId", "in", employees).where("skillId", "==", skillId).stream()

    # Initialize counters for each skill level
    skill_levels = {level: 0 for level in range(1, 6)}

    # Count occurrences of each skill level
    for doc in query_skills:
        current_doc = doc.to_dict()
        level = current_doc.get("level")
        if level in skill_levels:
            skill_levels[level] += 1

    return skill_levels

def getDepartamentNameRepo(employeeId):

    query = departamentManagerCollection.where("employeeId","==",employeeId).get()

    departamentId = []
    for doc in query:
        departamentId.append(doc.to_dict()["departamentId"])

    if not departamentId:
        raise CustomException(404,"Departament not found")

    query = departamentCollection.where("id","in",departamentId).get()

    departaments = []

    for doc in query:
        currentDoc = doc.to_dict()
        departaments.append(currentDoc)

    if not departaments:
        raise CustomException(404,"Departaments not found")

    return departaments




