from Domain.extension import technologyStackCollection


def postTechnologyStackRepo(technology):

    insertedItm = technologyStackCollection.document()
    insertedItmId = insertedItm.id

    technology["id"] = insertedItmId

    technologyStackCollection.add(technology)

    return technology