import requests
import os

import openai

from dotenv import load_dotenv

load_dotenv()
# def perplexity(source, destination, age):
#     url = os.getenv("PERPLEXITY_API_URL")
#     token = os.getenv("PERPLEXITY_API_KEY")
    
#     headers = {
#         'Authorization' : f'Bearer {token}',
#         'Content-Type': 'application/json'
#     }
    
#     data = {
#         "model": "llama-3.1-sonar-small-128k-online",
#         "messages": [
#             {
#             "role": "system",
#             "content": "You are a Visa Travel Expert. You help people with their documents required for Visa applications." 
#                             +"Only give information for Tourist Visa."
#                             +"You will be given from country and to country and you will have to provide documents required for the traveler." 
#                             +"Get the latest data and provide the visa requirements documents in points."
#             },
#             {
#             "role": "user",
#             "content": f"For {source} to {destination} age {age}"
#             }
#         ]
#     }
    
#     response = requests.post(url, headers=headers, json=data)
#     response=response.json()
#     print(response.get('choices')[0].get('message').get('content'))
#     return response.get('choices')[0].get('message').get('content')


# def test_openai_perplexity():
#     openai_api_key = os.getenv("OPENAI_API_KEY")
    
#     url = "https://api.openai.com/v1/chat/completions"
    
#     headers = {
#         "Content-Type" : "application/json",
#         "Authorization" : f"Bearer {openai_api_key}",
#     }    
    
#     data = {
#         "model": "gpt-4o",
#         "messages": [
#             {
#                 "role": "system",
#                 "content": "You are a Visa Travel Expert. You help people with their Visa applications." 
#                             +"Only give information for Tourist Visa."
#                             +"You will be given from country and to country and you will have to provide the visa requirements for the traveler." 
#                             +"You can also ask for the purpose of the travel. You can ask for the duration of the stay." 
#                             +"Get the latest data and provide the visa requirements in points."
#             },
#             {
#                 "role": "user",
#                 "content": "From India to USA age 26"
#             }
#         ],
#         "tools": [
#             {
#                 "type" : "function",
#                 "function": {
#                     "name": "get_visa_requirements",
#                     "description": "Get Visa Requirements for a traveler",
#                     "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "location": {
#                             "type": "string",
#                             "description": "The city and state, e.g. San Francisco, CA"
#                             },
#                         "unit": {
#                             "type": "string",
#                             "enum": ["celsius", "fahrenheit"]
#                             }
#                         },
#                     "required": ["location"]
#                     }
#                 }
#             }
#         ]
#     }


# from openai import OpenAI

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# visa_requirements = perplexity("Croatia", "South Korea", 26)

# completion = client.chat.completions.create(
#     model="gpt-4o",
#     messages=[
#         {"role": "system", "content": "You are a Visa Travel Documents check list maker. You help people with their Visa applications." 
#          +"Convert this data into a check list and give in json format with title and description."},
#         {"role": "user", "content": f"{visa_requirements}"}
#     ]
# )

# print(completion.choices[0].message.content)


def perplexity(source, destination):
    url = os.getenv("PERPLEXITY_API_URL")
    token = os.getenv("PERPLEXITY_API_KEY")
    
    headers = {
        'Authorization' : f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {
            "role": "system",
            "content": "You are a Visa Expert. Give the probability by nationality of getting a visa for a specific country."+
                        "For getting a Tourist visa. Just only give in Percentage format. keep it simple."
            },
            {
            "role": "user",
            "content": f"For {source} to {destination}"
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    response=response.json()
    print(response.get('choices')[0].get('message').get('content'))
    return response.get('choices')[0].get('message').get('content')


# perplexity("India", "USA", 26)

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

visa_requirements = perplexity("India", "USA")

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a Visa Travel Expert. Just give the probability percentage of getting a visa for a specific country."},
        {"role": "user", "content": f"{visa_requirements}"}
    ]
)

print(completion.choices[0].message.content)