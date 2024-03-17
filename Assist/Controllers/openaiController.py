
from flask import abort
from flask_restx import Namespace, Resource
from Application.Dtos.expect.openAiExpect import openAiExpect
from Domain.extension import api
from Utils.Exceptions.customException import CustomException
from Utils.OpenAI.openAi import getResponseFromChat,getMatchEmployees

nsOpenAi = Namespace("openai", description="Open AI")

@nsOpenAi.route("/")
class OpenAi(Resource):
    @nsOpenAi.expect(openAiExpect)
    def post(self):
        try:

            result = getResponseFromChat(api.payload)

            return {"message" : result},201
        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception as e:
            abort(500, "Something went wrong")
