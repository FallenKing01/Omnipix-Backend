from flask_restx import fields

from Domain.extension import api

departamentPostExpect = api.model("Departament post expect",
                            {
                                "name":fields.String,
                                "organizationId":fields.String,
                                "employeeId":fields.String,
                            })
