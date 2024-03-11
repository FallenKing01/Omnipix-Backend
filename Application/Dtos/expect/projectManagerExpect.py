from flask_restx import fields
from Domain.extension import api

technologyStackExpect = api.model("technology stack post",{
    "name":fields.String,
    "organizationId":fields.String,
})