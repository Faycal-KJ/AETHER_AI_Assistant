
#=============Libraries===========
import json
import requests




#===============Fetching Assistant Answer To User=================
def Fetch_Respone(AI_Key,user,Personality):


  #================Reading Updated Memory====================
  Temp_Mem = open("Memory/Temp_Mem.txt","r",encoding="utf-8").read()
  Core_Mem = open("Memory/Core_Mem.txt","r",encoding="utf-8").read()


  print("User: ",user)

  #============Input===================
  if user == "[User Input]:":
     user = "[User Woke you up but didn't say anything]"
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


  #===============Output====================
  if response.status_code == 200:
      print(" AI Response:", response.json()["choices"][0]["message"]["content"])
      return response.json()["choices"][0]["message"]["content"]
  else:
      print(f" Error {response.status_code}: {response.text}")



#=============Sumerising/Using Temp Memory to Update Core Memory==========
def Summerise(AI_Key,user):
  Temp_Mem = open("Memory/Temp_Mem.txt","r",encoding="utf-8").read()
  Core_Mem = open("Memory/Core_Mem.txt","r",encoding="utf-8").read()

  #=================Input=====================
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
  
  #==================Ouput=====================
  if response.status_code == 200:
      return response.json()["choices"][0]["message"]["content"]
  else:
      print(f" Error {response.status_code}: {response.text}")
