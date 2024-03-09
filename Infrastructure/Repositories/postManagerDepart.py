from Domain.extension import departamentManagerCollection
def createDepartManRepo(employee):

    insertItm = departamentManagerCollection.document()
    insertItmId = insertItm.id

    employee["id"] = insertItmId
    employee["departamentId"]=None

    departamentManagerCollection.add(employee)

    return employee