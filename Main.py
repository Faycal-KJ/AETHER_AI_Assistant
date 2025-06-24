import os
import sys
import STT
import TTS
import signal
import WakeWord
import threading
import Load_Model
import SpeechRec
import subprocess
from dotenv import load_dotenv

load_dotenv()

Speech = ''
CMD_WHITELIST = set([
    "shutdown", "kill", "start", "type", "findstr", "dir", "cd", "systeminfo",
    "hostname", "whoami", "ver", "wmic cpu get name", "wmic os get Caption",
    "wmic memorychip get capacity", "tasklist", "taskmgr", "resmon", "perfmon",
    "powershell Get-Process", "powershell Get-ComputerInfo", "ping www.google.com",
    "ipconfig", "ipconfig /all", "netstat -e", "tracert www.google.com",
    "powershell Test-NetConnection google.com", "date /T", "time /T", "echo", "cls", "set"
])


Prompt = open("Prompt.txt","r",encoding="utf-8").read()
Personality = open("Personality.txt","r",encoding="utf-8").read()

Access_Key = os.getenv("API_KEY")
AI_Key = os.getenv("AI_Key")
def Transcribtion(Recording):
  global Speech
  Speech = STT.Transcribe(Recording)
def Run_Command(command):
  for i in CMD_WHITELIST:
    if i in command:
      subprocess.run(command[5:],shell=True)

def WakeUp():
  global Speech
  print("Waking Up!")
  Recording = SpeechRec.Record()
  T1 = threading.Thread(target=Transcribtion(Recording), args=(Recording,))
  T1.start()
  T1.join()
  Ai_Speech = Load_Model.Fetch_Respone(AI_Key,Speech,Prompt,Personality)
  if "@@" in Ai_Speech:
    Speech_part,Command_part = Ai_Speech.split("@@")
  else:
    Speech_part = Ai_Speech
    Command_part = ""
  threading.Thread(target=Run_Command(Command_part)).start()
  threading.Thread(target=TTS.Say(Speech_part)).start()
  if "@\@\@" not in Ai_Speech:
    WakeUp()

  # def Exit(sig,frame):
  #   WakeWord.keep_running.set()
  #   WakeWord.por.delete()
  #   sys.exit(0)

  # signal.signal(signal.SIGINT,Exit)

WakeWord.start_Listening(WakeUp=WakeUp)