
#=============Libraries===========
import json
import requests
import os

AI_Key = os.getenv("AI_Key")


#===============Fetching Assistant Answer To User=================
def Fetch_Respone(user,Personality):

  #================Reading Updated Memory====================
  Temp_Mem = open("Memory/Temp_Mem.txt","r",encoding="utf-8").read()
  Core_Mem = open("Memory/Core_Mem.txt","r",encoding="utf-8").read()
  Sys_Info = open("Memory/System_info.txt","r",encoding="utf-8").read()


  #============Input===================
  if user == "[User Input]:":
     user = "..."
  response = requests.post(
    url="https://api.groq.com/openai/v1/chat/completions",
    headers={
      "Authorization": f"Bearer {AI_Key}",
      "Content-Type": "application/json"
    },
    data=json.dumps({
      "model": "meta-llama/llama-4-scout-17b-16e-instruct",
      "messages": [
        {
        "role": "user",
        "content": [
            {"type": "text", "text": f"""{Personality}\n[Core Memory]:{Core_Mem}\n[End of Core Memory]\n[Previous Chats in the session]\n{Temp_Mem}\n[End of Previous Chats]\n[System Info]\n{Sys_Info}\n[End of System Info]\n\n{user}"""}
          ]
        }
      ],
      "temperature": 0.7
    })
  )
      


  #===============Output====================
  if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
  else:
      print(f" Error {response.status_code}: {response.text}")

