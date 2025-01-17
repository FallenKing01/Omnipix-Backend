from flask_restx import fields

from Domain.extension import api

employeePostExpect = api.model("Employee post expect",
                            {
                                "name":fields.String,
                                "email": fields.String,
                                "password": fields.String,
                                "organizationId":fields.String
                            })

endorsement = api.model("Endorsement", {
    "title": fields.String,
    "description": fields.String,
})

# Define the Assign skill model with a list of endorsements
assignSkill = api.model("Assign skill", {
    "employeeId": fields.String,
    "skillId": fields.String,
    "level": fields.Integer,
    "experience": fields.Integer,
    "endorsements": fields.List(fields.Nested(endorsement)),
    "projectId":fields.List(fields.String),
})

assignDepartament = api.model("Assign departament",{
    "employeeId": fields.String,
    "departamentId":fields.String,
})

postProjectSkill = api.model("Post project skill",{
    "projectId" :fields.String,
    "skillId": fields.String,
    "minimumLevel": fields.Integer,
})