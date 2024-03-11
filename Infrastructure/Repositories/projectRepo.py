from Domain.extension import projectCollection,projectStatusCollection
from Infrastructure.Repositories.ProjectManagerRepo import updateProjectsOfManager
from datetime import datetime

def postProjectRepo(project):

    insertedItm = projectCollection.document()
    insertedItmId = insertedItm.id

    updateProjects = {
        "employeeId":project["employeeId"],
        "projectId":insertedItmId
    }

    projectStatus = {
        "projectId": insertedItmId,
        "status":project["status"],
        "creationDate": datetime.utcnow()
    }

    project.pop("status")
    updateProjectsOfManager(updateProjects)

    project["id"] = insertedItmId

    projectStatusCollection.add(projectStatus)
    projectCollection.add(project)

    return project

def updateProjectRepo(project):
    # Find the document(s) matching the project ID
    query = projectCollection.where("id", "==", project["projectId"])
    docs = query.get()

    # Get the technologies and team roles to delete and add
    technologyToDelete = project.get("technologyToDelete", [])
    technologyToAdd = project.get("technologyToAdd", [])
    teamRolesToAdd = project.get("teamRolesToAdd", [])
    teamRolesToDelete = project.get("teamRolesToDelete", [])

    # Iterate over the matching documents
    for doc in docs:
        # Update common fields
        doc.reference.update({
            "status": project["status"],
            "name": project["name"],
            "period": project["period"],
            "startDate": project["startDate"],
            "description": project["description"],
        })

        # Retrieve current technology stack from the document
        current_technology_stack = doc.to_dict().get("technologyStack", [])

        # Remove technologies from the technology stack
        for tech in technologyToDelete:
            if tech in current_technology_stack:
                current_technology_stack.remove(tech)

        # Add new technologies to the technology stack
        for tech in technologyToAdd:
            current_technology_stack.append(tech)

        # Update the document with the modified technology stack
        doc.reference.update({
            "technologyStack": current_technology_stack
        })

        # Retrieve current team roles from the document
        current_team_roles = doc.to_dict().get("teamRoles", {})

        # Remove team roles from the team roles list
        for role_id in teamRolesToDelete:
            if role_id in current_team_roles:
                del current_team_roles[role_id]

        # Add new team roles to the team roles list
        current_team_roles.update(teamRolesToAdd)

        # Update the document with the modified team roles
        doc.reference.update({
            "teamRoles": current_team_roles
        })