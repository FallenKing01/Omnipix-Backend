from flask_restx import fields
from Domain.extension import api

skillPostExpect = api.model("Skill post expect",
                            {
                                "category":fields.String,
                                "name":fields.String,
                                "description":fields.String,
                                "authorId":fields.String,
                                "organizationId":fields.String
                            })

skillUpdateExpect = api.model("Skill update expect",
                              {
                                  "skillId":fields.String,
                                  "managerId":fields.String,
                                  "name":fields.String,
                                  "category":fields.String,
                                  "description":fields.String,
                              })