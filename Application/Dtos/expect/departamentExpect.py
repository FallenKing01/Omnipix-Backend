from flask_restx import fields

from Domain.extension import api

departamentPostExpectWithManager = api.model("Departament post expect with manager",{
                                "name":fields.String,
                                "organizationId":fields.String,
                                "employeeId":fields.String,
                            })

departamentPostExpect = api.model("Departament post expect",{
                                "name":fields.String,
                                "organizationId":fields.String,
                            })

promoteDepartamentManager = api.model("Promote to departament manager",{
                                "employeeId":fields.String,
                                "departamentId":fields.String,
                            })
postDepartamentSkills = api.model("Departament skill",{
                                "skillId":fields.String,
                                "departamentId":fields.String
})