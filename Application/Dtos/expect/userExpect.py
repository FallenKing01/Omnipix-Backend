from flask_restx import fields

from Domain.extension import api

userPostExpect = api.model("User post expect",
                            {
                                "email": fields.String,
                                "password": fields.String,
                                "role": fields.String
                            })
