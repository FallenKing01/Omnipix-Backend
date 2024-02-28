from flask_restx import fields

from Domain.extension import api

loginExpect = api.model("Login post",
                            {
                                "email": fields.String,
                                "password": fields.String,
                            })
