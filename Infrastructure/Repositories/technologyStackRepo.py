from Domain.extension import technologyStackCollection


def postTechnologyStackRepo(technology):

    insertedItm = technologyStackCollection.document()
    insertedItmId = insertedItm.id

    technology["id"] = insertedItmId

    technologyStackCollection.add(technology)

    return technology

def getTechnologyStackRepo(organizationId):

    query = technologyStackCollection.where("organizationId", "==", organizationId).get()

    technologyStacks = []

    if query:
        for doc in query:
            technologyStack = doc.to_dict()
            technologyStacks.append(technologyStack)

    return technologyStacks