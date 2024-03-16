from flask_restx import fields
from Domain.extension import api

technologyStackExpect = api.model("technology stack post",{
    "name":fields.String,
    "organizationId":fields.String,
})

postSkillCategory = api.model("category post",{
    "skillId":fields.String,
    "name":fields.String,
    "departamentId":fields.String,
    "organizationId":fields.String,
})
