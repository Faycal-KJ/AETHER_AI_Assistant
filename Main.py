import os
import Convo.STT as STT
import Convo.TTS as TTS
import WakeWord
import threading
import Model.Load_Model as Load_Model
import Convo.SpeechRec as SpeechRec
import subprocess
from datetime import datetime
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
Personality = open("Personality.txt","r",encoding="utf-8").read()

Access_Key = os.getenv("API_KEY")
AI_Key = os.getenv("AI_Key")
OpenAI_Key = os.getenv("OpenAI_Key")
def Transcribtion(Recording):
  global Speech
  Speech = STT.Transcribe(Recording)
def Run_Command(command):
  for i in CMD_WHITELIST:
    if i in command:
      C = subprocess.run(command[5:],capture_output=True,shell=True,text=True)
      with open("Temp_Mem.txt","a",encoding="utf-8") as f:
       f.write(f"[System]:\n{C.stdout}\n")
def WakeUp():
  global Speech
  print("Waking Up!")
  Recording = SpeechRec.Record()
  T1 = threading.Thread(target=Transcribtion(Recording), args=(Recording,))
  T1.start()
  T1.join()
  Ai_Speech = Load_Model.Fetch_Respone(OpenAI_Key,"[User Input]:" + Speech,Personality)
  if "@@" in Ai_Speech:
    Speech_part,Command_part = Ai_Speech.split("@@")
    threading.Thread(target=Run_Command(Command_part))
  else:
    Speech_part = Ai_Speech
  threading.Thread(target=TTS.Say(Speech_part)).start()
  with open("Temp_Mem.txt","a",encoding="utf-8") as f:
   f.write(f"[{datetime.now()}]\n[User]:{Speech}\n[Aether]:{Ai_Speech}\n")
  if "@\@\@" not in Ai_Speech:
    WakeUp()
  else:
    Summerise_memory()
def Summerise_memory():
  Summery = Load_Model.Summerise(AI_Key,"""You are now presented with a conversation between Aether(an Ai assistant) and the user.
                                     
                                     Take Any important information about (the user,the system,the pc..etc) or any rules he implied (that arent already written in The Core Memory Part) from the Previous chat part and put them into bullet points.
  
                                 
                                Answer Format Example:

                                [the dat the memory started and the today date]
                                -user is working out
                                -user had a problem in thier pc
                                -user told Aether to never say donut""")
  with open("Core_Mem.txt","w",encoding="utf-8") as f: 
    f.write(Summery)
  with open("Temp_Mem.txt","w",encoding="utf-8") as f:
    f.write("")
WakeWord.start_Listening(WakeUp=WakeUp)