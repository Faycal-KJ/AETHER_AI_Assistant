import os
import WakeWord
from dotenv import load_dotenv

load_dotenv()

Access_Key = os.getenv("API_KEY")

def WakeUp():
  print("Im Awake!")

WakeWord.start_Listening(Access_Key=Access_Key,WakeUp=WakeUp)