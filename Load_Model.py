import json
import requests


def Fetch_Respone(AI_Key,user):
  print("User: ",user)
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
          "content": f"{user}"
        }
      ]
    })
  )
  
  if response.status_code == 200:
      print(" AI Response:", response.json()["choices"][0]["message"]["content"])
  else:
      print(f" Error {response.status_code}: {response.text}")
