from flask_restx import fields

from Domain.extension import api

employeePostExpect = api.model("Employee post expect",
                            {
                                "name":fields.String,
                                "email": fields.String,
                                "password": fields.String,
                                "organizationId":fields.String
                            })
