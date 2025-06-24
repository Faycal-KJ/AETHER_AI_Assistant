import json
import requests

def Fetch_Respone(AI_Key,user,Prompt,Personality):
  print("User: ",user)
  if not user:
     user = "User Woke you up but didn't say anything"
  response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
      "Authorization": f"Bearer {AI_Key}",
      "Content-Type": "application/json"
    },
    data=json.dumps({
      "model": "google/gemini-flash-1.5-8b",
      "messages": [
        {
          "role": "user",
          "content": f"""{Personality}\n{Prompt}\n{user}"""
        }
      ]
    })
  )
  if response.status_code == 200:
      print(" AI Response:", response.json()["choices"][0]["message"]["content"])
      return response.json()["choices"][0]["message"]["content"]
  else:
      print(f" Error {response.status_code}: {response.text}")
