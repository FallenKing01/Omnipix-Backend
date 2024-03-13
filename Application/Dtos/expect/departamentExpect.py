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

updateManagerExpect = api.model("Update departament manager ",{
    "departamentId":fields.String,
    "employeeId":fields.String,
})

updateDepartamentNameExpect = api.model("Update departament name ",{
    "departamentId":fields.String,
    "name":fields.String,
})
postDepartamentManagerExpect = api.model("Post departament manager",{
    "employeeId":fields.String,
    "organizationId":fields.String,
})

acceptProposalExpect = api.model("Accept proposal",{
    "projectId": fields.String,
    "assignementProposalId": fields.String,
    "employeeId": fields.String,
    "organizationId" : fields.String,
    "workingHours":fields.Integer,
    "employeRolesId":fields.List(fields.String),
    "isActive":fields.Boolean
})

dealocationProposalExpect = api.model("Dealocation proposal",{
    "projectId": fields.String,
    "employeeId": fields.String,
    "reason": fields.String,
    "departamentId": fields.String,
})

acceptDealocationProposal = api.model("Accept dealocation proposal" , {
    "projectId": fields.String,
    "employeeId": fields.String,
    "reason": fields.String,
    "departamentId": fields.String,
    "dealocatedId":fields.String,
})