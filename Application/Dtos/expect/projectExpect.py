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
    "status": fields.String,
    "organizationId": fields.String,
    "employeeId": fields.String
})

updateProjectStatus = api.model("Update project status", {
    "projectId": fields.String,
    "status": fields.String,
})

updateProjectExpect = api.model("Update project", {
    "projectId": fields.String,
    "status": fields.String,
    "name": fields.String,
    "period": fields.String,
    "startDate": fields.DateTime,
    "deadlineDate": fields.DateTime,
    "description": fields.String,
    "technologyStack": fields.List(fields.String),
    "teamRoles": fields.Raw,  # Using Raw field to accept any JSON structure
})

assignmentProposalExpect = api.model("Assignment proposal", {
    "projectId": fields.String,
    "employeeId": fields.String,
    "numberOfHours": fields.Integer,
    "teamRolesId": fields.List(fields.String),
    "comment": fields.String,
    "departamentId": fields.String,

})
