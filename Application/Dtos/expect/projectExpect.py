from flask_restx import fields
from Domain.extension import api

postProjectExpect = api.model("Create project", {
    "name": fields.String,
    "period": fields.String,
    "startDate": fields.DateTime,
    "deadlineDate": fields.DateTime,
    "description": fields.String,
    "technologyStack": fields.List(fields.String),
    "teamRoles": fields.Raw,  # Using Raw field to accept any JSON structure
    "status": fields.Boolean,
    "organizationId": fields.String,
    "employeeId":fields.String
})



updateProjectStatus = api.model("Update project status" , {
    "projectId":fields.String,
    "status":fields.String,
})
updateProjectExpect =api.model("Update project", {
    "projectId":fields.String,
    "status":fields.Boolean,
    "name": fields.String,
    "period": fields.String,
    "startDate": fields.DateTime,
    "deadlineDate": fields.DateTime,
    "description": fields.String,
    "technologyToDelete": fields.List(fields.String),
    "technologyToAdd": fields.List(fields.String),
    "teamRolesToAdd": fields.Raw,
    "teamRolesToDelete": fields.Raw,
})

assignmentProposalExpect =api.model("Assignment proposal", {
    "projectId":fields.String,
    "employeeId":fields.String,
    "numberOfHours":fields.Integer,
    "teamRolesId": fields.List(fields.String),
    "comment":fields.String,
    "departamentId":fields.String,

})

