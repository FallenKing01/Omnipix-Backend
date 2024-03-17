from flask_restx import fields

from Domain.extension import api

openAiExpect = api.model('openAiExpect', {
    "content": fields.String(required=True),
    "organizationId": fields.String(required=True),
})