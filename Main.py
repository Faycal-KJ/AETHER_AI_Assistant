import os
import WakeWord
import threading
import Load_Model

from dotenv import load_dotenv

load_dotenv()

Access_Key = os.getenv("API_KEY")
AI_Key = os.getenv("AI_Key")

def Fetch_Answer():
  Load_Model.Fetch_Respone(AI_Key)  

def WakeUp():
  print("Waking Up!")
  threading.Thread(target=Fetch_Answer).start()

WakeWord.start_Listening(Access_Key=Access_Key,WakeUp=WakeUp)