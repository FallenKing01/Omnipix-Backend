from openai import AzureOpenAI
from Domain.extension import assignedSkillCollection,employeesCollection,skillCollection
import json

def getMatchEmployees(organizationId):
    employeesQuery = employeesCollection.where("organizationId", "==", organizationId).get()
    employees = []
    employeesId = []
    result = []
    if employeesQuery:
        for doc in employeesQuery:
            currentDoc = doc.to_dict()
            currentDoc.pop("password", None)
            employeesId.append(currentDoc["id"])
            employees.append(currentDoc)
    assignedSkillQuery = assignedSkillCollection.where("employeeId", "in", employeesId).get()
    assignedSkills = []
    if assignedSkillQuery:
        for doc in assignedSkillQuery:
            currentDoc = doc.to_dict()
            assignedSkills.append(currentDoc)

        for doc in assignedSkills:
            if doc["isApproved"] == True:
                finalResponse = {}  # Create a new dictionary for each iteration
                finalResponse["level"] = doc["level"]
                finalResponse["employeeId"] = doc["employeeId"]
                finalResponse["departamentId"] = doc["departamentId"]

                # Check if "experience" key exists in currentDoc before accessing it
                if "experience" in currentDoc:
                    finalResponse["experience"] = currentDoc["experience"]

                skillQuery = skillCollection.where("id", "==", doc["skillId"]).get()
                skill = []
                if skillQuery:
                    for docSkill in skillQuery:
                        currentSkill = docSkill.to_dict()
                        finalResponse["skillName"] = currentSkill["name"]
                        skill.append(currentSkill)

                for docEmployee in employees:
                    if doc["employeeId"] == docEmployee["id"]:
                        finalResponse["email"] = docEmployee["email"]
                        finalResponse["workingHours"] = docEmployee["workingHours"]

                result.append(finalResponse)
    return result





def getResponseFromChat(data):
    api_key = "ded4845c62e94742896cccf6dad671ee"
    x = getMatchEmployees(data["organizationId"])
    data["content"] = data["content"] + "din datele" + str(x)
    print(x)

    message_text = [
        {"role": "system", "content": "You are a very helpful assistant. You respond only in json format."},
        {"role": "user", "content": data["content"]}  # Remove 'description' property
    ]

    client = AzureOpenAI(
        azure_endpoint="https://sweden-central-openai-demo.openai.azure.com/",
        api_key=api_key,
        api_version="2024-02-15-preview"
    )

    completion = client.chat.completions.create(
        model="gpt4",
        messages=message_text,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )

    # Access the JSON string within the ChatCompletionMessage object
    completion_message_json = completion.choices[0].message.content

    # Parse the JSON string
    message_json = json.loads(completion_message_json)

    # Check if the response contains information about employees
    if "employees" in message_json.get("message", {}):
        return []  # Return an empty list if employee information is present
    else:
        return message_json
