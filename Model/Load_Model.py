
#=============Libraries===========
import json
import requests
import traceback
import os

AI_Key = os.getenv("AI_Key")


#===============Fetching Assistant Answer To User=================
def Fetch_Respone(user,Personality):
  print("User: ",user)

  #================Reading Updated Memory====================
  Temp_Mem = open("Memory/Temp_Mem.txt","r",encoding="utf-8").read()
  Core_Mem = open("Memory/Core_Mem.txt","r",encoding="utf-8").read()
  Description = open("Memory/Screen_Description.txt","r",encoding="utf-8").read()


  #============Input===================
  if user == "[User Input]:":
     user = "..."
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
        "content": [
            {"type": "text", "text": f"""{Personality}\n[Core Memory]:{Core_Mem}\n[End of Core Memory]\n[Previous Chats in the session]\n{Temp_Mem}\n[End of Previous Chats]\n[Screen Description]{Description}[End of Screen Description]\n{user}"""}
          ]
        }
      ]
    })
  )
      


  #===============Output====================
  if response.status_code == 200:
        print(" AI Response:", response.json()["choices"][0]["message"]["content"])
        return response.json()["choices"][0]["message"]["content"]
  else:
      print(f" Error {response.status_code}: {response.text}")

