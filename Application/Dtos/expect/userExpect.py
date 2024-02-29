from flask_restx import fields

from Domain.extension import api

userPostExpect = api.model("User post expect",
                            {
                                "name":fields.String,
                                "email": fields.String,
                                "password": fields.String,
                                "organizationId":fields.String,
                                "departamentId":fields.String
                            })
