import json
import requests

def Fetch_Respone(AI_Key,user,Personality):
  Temp_Mem = open("Temp_Mem.txt","r",encoding="utf-8").read()
  Core_Mem = open("Core_Mem.txt","r",encoding="utf-8").read()
  print("User: ",user)
  if user == "[User Input]:":
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
          "content": f"""{Personality}\n[Core Memory]:{Core_Mem}\n[End of Core Memory]\n[Previous Chats in the session]\n{Temp_Mem}\n[End of Previous Chats]\n\n{user}"""
        }
      ]
    })
  )
  if response.status_code == 200:
      print(" AI Response:", response.json()["choices"][0]["message"]["content"])
      return response.json()["choices"][0]["message"]["content"]
  else:
      print(f" Error {response.status_code}: {response.text}")

      
def Summerise(AI_Key,user):
  Temp_Mem = open("Temp_Mem.txt","r",encoding="utf-8").read()
  Core_Mem = open("Core_Mem.txt","r",encoding="utf-8").read()
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
          "content": f"""[Core Memory]:{Core_Mem}\n[End of Core Memory]\n[Previous Chats in the session]\n{Temp_Mem}\n[End of Previous Chats]\n\n{user}"""
        }
      ]
    })
)
  if response.status_code == 200:
      return response.json()["choices"][0]["message"]["content"]
  else:
      print(f" Error {response.status_code}: {response.text}")
