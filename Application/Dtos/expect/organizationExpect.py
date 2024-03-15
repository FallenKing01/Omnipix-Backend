from flask_restx import fields
from Domain.extension import api

organizationPostExpect = api.model("Organization post expect",
                                   {
                                       "name": fields.String,
                                       "adress": fields.String,
                                       "entranceUrl": fields.String,

                                   })
