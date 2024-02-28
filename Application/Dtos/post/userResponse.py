from flask_restx import fields

from Domain.extension import api

userPostResponse = api.model("User post response",
                            {
                                "id":fields.String,
                                "email": fields.String,
                                "password": fields.String,
                                "role": fields.String
                            })