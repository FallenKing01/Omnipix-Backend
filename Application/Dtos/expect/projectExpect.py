from flask_restx import fields
from Domain.extension import api

postProjectExpect = api.model("Create project" , {
    "name":fields.String,
    "period":fields.String,
    "startDate":fields.DateTime,
    "deadlineDate":fields.DateTime,
    "description":fields.String,

})

