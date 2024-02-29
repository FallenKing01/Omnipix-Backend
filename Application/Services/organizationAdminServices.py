from Infrastructure.Repositories.OrganizationAdminRepo import *

def postOrganizationService(organizationAdmin):

    organizationAdmin = postOrganizationAdminRepository(organizationAdmin)

    return organizationAdmin