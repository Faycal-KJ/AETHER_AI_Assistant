import os
import sys
import STT
import TTS
import signal
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
  Ai_Speech = Load_Model.Fetch_Respone(AI_Key,Speech)
  T1 = threading.Thread(target=TTS.Say(Ai_Speech))
  WakeWord.start_Listening(WakeUp=WakeUp)

  def Exit(sig,frame):
    WakeWord.keep_running.set()
    WakeWord.por.delete()
    sys.exit(0)

  signal.signal(signal.SIGINT,Exit)

WakeWord.start_Listening(WakeUp=WakeUp)