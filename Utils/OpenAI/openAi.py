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
                finalResponse = {}
                finalResponse["level"] = doc["level"]
                finalResponse["id"] = doc["employeeId"]
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
    print(result)
    return result



def getResponseFromChat(data):
    api_key = "ded4845c62e94742896cccf6dad671ee"
    x = getMatchEmployees(data["organizationId"])
    data["content"] = (" avand lista de angajati de mai jos, "
                       "te rog sa imi raspunzi la intrebarea urmatoare. "
                       "In cazul in care nu gasesti, te rog da-mi un json "
                       '{"message":"Nu am gasit angajatul."},daca gasesti raspunde-mi {"message": "JSONUL CU ANGAJATII CARE SE POTRIVES"}  '
                       "foloseste doar setul meu de date. "
                       "Setul de date este: " + str(x) +
                       "Iar intrebarea este: " + data["content"])

    print(x)

    message_text = [
        {"role": "system", "content": "You respond only in json format."},
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

    return message_json
