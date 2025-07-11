
#=============Libraries===========
import json
import requests
import traceback



#===============Fetching Assistant Answer To User=================
def Fetch_Respone(AI_Key,user,Personality,image_url):


  #================Reading Updated Memory====================
  Temp_Mem = open("Memory/Temp_Mem.txt","r",encoding="utf-8").read()
  Core_Mem = open("Memory/Core_Mem.txt","r",encoding="utf-8").read()


  print("User: ",user)

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
          "content": f"""{Personality}\n[Core Memory]:{Core_Mem}\n[End of Core Memory]\n[Previous Chats in the session]\n{Temp_Mem}\n[End of Previous Chats]\n\n{user}"""
        },
        {
          "type": "image_url",
          "image_url": {
            "url": image_url
          }
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
def Summerise(AI_Key, user):
    Temp_Mem = open("Memory/Temp_Mem.txt", "r", encoding="utf-8").read()
    Core_Mem = open("Memory/Core_Mem.txt", "r", encoding="utf-8").read()
    try:
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
            print(f"Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print("Exception occurred in summary request:")
        traceback.print_exc()
        return None