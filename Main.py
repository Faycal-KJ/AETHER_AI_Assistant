import os
import STT
import WakeWord
import threading
import Load_Model
import SpeechRec
from dotenv import load_dotenv

load_dotenv()

Speech = ''

Access_Key = os.getenv("API_KEY")
AI_Key = os.getenv("AI_Key")
def Transcribtion(Recording):
  global Speech
  Speech = STT.Transcribe(Recording)
def WakeUp():
  global Speech
  print("Waking Up!")
  Recording = SpeechRec.Record()
  T1 = threading.Thread(target=Transcribtion(Recording), args=(Recording,))
  T1.start()
  T1.join()
  Load_Model.Fetch_Respone(AI_Key,Speech)  

WakeWord.start_Listening(WakeUp=WakeUp)