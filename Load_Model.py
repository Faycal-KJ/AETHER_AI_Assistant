import json
import requests


def Fetch_Respone(AI_Key):
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
          "content": "act like a home smart ai system that talks like jarvis,you have just been woken up by the owner like any usual day"
        }
      ]
    })
  )
  
  if response.status_code == 200:
      print(" AI Response:", response.json()["choices"][0]["message"]["content"])
  else:
      print(f" Error {response.status_code}: {response.text}")
