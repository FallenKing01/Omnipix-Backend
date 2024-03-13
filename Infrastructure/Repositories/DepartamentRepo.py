from Domain.extension import dealocationProposalCollection,projectXemployeeCollection,assignementProposalCollection,departamentManagerCollection,departamentCollection,employeesCollection,skillCollection
from Utils.Exceptions.customException import CustomException
def postDepartamentRepoADDITIONAL(depart):

    # IAU DOAR CE AM NEV PENTRU MANAGER
    managerDepartament = {
        "id" : depart["departamentManagerId"],
        "employeeId" : None,
        "departamentId": depart["departamentId"],
        "organizationId": depart["organizationId"]
    }

    departamentManagerCollection.add(managerDepartament)

    #RESTRUCTUREZ FORMA DEPARTAMENT SA ARATE CA IN TABELA
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
    query = departamentCollection.where("id", "==", id).limit(1).get()
    department = None

    for doc in query:
        department = doc.to_dict()
        break

    return department


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

    query = assignementProposalCollection.where("departamentId","==",departamentId).get()

    allocation = []

    for doc in query:
        currentDoc = doc.to_dict()
        allocation.append(currentDoc)

    return allocation

def getDealocationProposalRepo(departamentId):
    query = dealocationProposalCollection.where("departamentId", "==", departamentId).get()

    dealocations = []

    for doc in query:
        currentDoc = doc.to_dict()
        dealocations.append(currentDoc)

    return dealocations

