#=========Libraires===============
import os
import sys
import time
import threading
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image
import shlex
from pystray import Icon,Menu,MenuItem

#========Helper Scripts=============
import Convo.STT as STT
import Convo.TTS as TTS
import Startup_SYS.WakeWord as WakeWord
import Model.Load_Model as Load_Model
import Convo.SpeechRec as SpeechRec
import Vision.Vision_SYS as Vision_SYS

#===============Assets/Configurators===============
AI_ON_Image = Image.open("Assets/ON.png")
AI_OFF_Image = Image.open("Assets/OFF.png")
Personality = open("Personality/Personality.txt","r",encoding="utf-8").read()
Temp_Mem_File = open("Memory/Temp_Mem.txt", "a", encoding="utf-8", buffering=1)
CMD_WHITELIST = set([
    "shutdown", "kill", "start", "type", "findstr", "dir", "cd", "systeminfo",
    "hostname", "whoami", "ver", "wmic cpu get name", "wmic os get Caption",
    "wmic memorychip get capacity", "tasklist", "taskmgr", "resmon", "perfmon",
    "powershell Get-Process", "powershell Get-ComputerInfo", "ping www.google.com",
    "ipconfig", "ipconfig /all", "netstat -e", "tracert www.google.com",
    "powershell Test-NetConnection google.com", "date /T", "time /T", "echo", "cls", "set"
])
load_dotenv()


#============Toolbar Icon==============
def quit_app(icon, item):
    Summerise_memory()
    WakeWord.keep_running.set()
    print("Turning OFF Assistant")
    icon.stop()
    sys.exit(0)
icon = Icon("AI Assistant", AI_OFF_Image, menu=Menu(MenuItem("Quit", quit_app)))
def setup_tray():
  global icon
  icon.run()
def ON():
  global icon
  icon.icon = AI_ON_Image
def OFF():
  global icon
  icon.icon = AI_OFF_Image

def Describe():
  while True:
    Vision_SYS.Screenshot()
    time.sleep(0.2)
#==========Speech to Text function=======
def Transcribtion(Recording):
  Speech = STT.Transcribe(Recording)
  return Speech

#==========Run AI cammands===============
def Run_Command(command):
  if any(command.strip().startswith(w) for w in CMD_WHITELIST):
      arg = shlex.split(command[5:])
      C = subprocess.run(arg,capture_output=True,text=True)
      Temp_Mem_File.write(f"[System]:\n{C.stdout}\n")
#==============Main System==============
def WakeUp():
  print("Woke Up!")

  #============Record User's Speech=============
  threading.Thread(target=ON,daemon=True).start()
  """
  Recording = SpeechRec.Record()


  #======STT(Transcribe Speech to Text)=========
  Speech = Transcribtion(Recording)

  """
  Speech = input("User: ")
  #============Getting AI response==============
  Ai_Speech = Load_Model.Fetch_Respone("[User Input]:" + Speech,Personality)


  #===============Handle Response===============
  if "@@" in Ai_Speech:
    Speech_part,Command_part = Ai_Speech.split("@@")
    threading.Thread(target=Run_Command, args=(Command_part,)).start()
  else:
    Speech_part = Ai_Speech
  if "@\@\@" in Speech_part:
    Speech_part,A = Speech_part.split("@\@\@")
  threading.Thread(target=TTS.Say, args=(Speech_part,)).start()
  #=======Saving History of Conversation(Temp Memory)=======
  Temp_Mem_File.write(f"[{datetime.now()}]\n[User]:{Speech}\n[Aether]:{Ai_Speech}\n")

  #==========Checking if Assistant should shut down===========
  if "@\@\@" not in Ai_Speech:
    WakeUp()
  else:
    threading.Thread(target=OFF,daemon=True).start()


#==============Save memory before shutting down==============
def Summerise_memory():
  Summery = Load_Model.Fetch_Respone("""You are now presented with a conversation between Aether(an Ai assistant) and the user.
                                     
                                     Take Any important information about (the user,the system,the pc..etc) or any rules he implied (that arent already written in The Core Memory Part) from the Previous chat part and put them into bullet points.
  
                                 
                                Answer Format Example:

                                [the date the memory started and the today date]
                                -user is working out
                                -user had a problem in thier pc
                                -user told Aether to never say donut""","")
  #==========Save Summery of session into memory=============
  with open("Memory/Core_Mem.txt","w",encoding="utf-8") as f: 
    f.write(Summery)
  #===================Clean Temp Memory======================
  with open("Memory/Temp_Mem.txt","w",encoding="utf-8") as f:
    f.write("")
  Temp_Mem_File.flush()
  Temp_Mem_File.close()
threading.Thread(target=setup_tray,daemon=True).start()
threading.Thread(target=Describe).start()
WakeWord.start_Listening(WakeUp=WakeUp)