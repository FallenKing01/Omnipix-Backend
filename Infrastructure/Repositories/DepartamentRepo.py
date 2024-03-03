from Domain.extension import departamentManagerCollection,departamentCollection

def postDepartamentRepo(depart):

    # IAU DOAR CE AM NEV PENTRU MANAGER
    managerDepartament = {
        "id" : depart["departamentManagerId"],
        "employeeId" : depart["employeeId"],
        "departamentId": depart["departamentId"]
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
