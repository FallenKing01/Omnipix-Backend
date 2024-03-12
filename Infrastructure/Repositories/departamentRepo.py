from Domain.extension import departamentManagerCollection,departamentCollection,employeesCollection,skillCollection
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
    query = departamentManagerCollection.where('organizationId', '==', id).where('departamentId', '==', None)
    managerDocs = query.stream()

    employeeIds = []

    for doc in managerDocs:
        employeeIds.append(doc.to_dict()['employeeId'])

    employees = employeesCollection.where('id', 'in', employeeIds).stream()

    employeeData = []

    for employee in employees:
        employeeDict = employee.to_dict()

        employeeDict.pop('password')
        employeeData.append(employeeDict)

    return employeeData




