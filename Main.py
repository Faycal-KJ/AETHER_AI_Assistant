#=========Libraires===============
import os
import threading
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image
from pystray import Icon,Menu,MenuItem


#========Helper Scripts=============
import Convo.STT as STT
import Convo.TTS as TTS
import Startup_SYS.WakeWord as WakeWord
import Model.Load_Model as Load_Model
import Convo.SpeechRec as SpeechRec


#===============Assets/Configurators===============
AI_ON_Image = Image.open("Assets/ON.png")
AI_OFF_Image = Image.open("Assets/OFF.png")
Personality = open("Personality/Personality.txt","r",encoding="utf-8").read()
Access_Key = os.getenv("API_KEY")
AI_Key = os.getenv("AI_Key")
OpenAI_Key = os.getenv("OpenAI_Key")
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
    icon.stop()
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


#==========Speech to Text function=======
def Transcribtion(Recording):
  Speech = STT.Transcribe(Recording)
  return Speech

#==========Run AI caommands===============
def Run_Command(command):
  for i in CMD_WHITELIST:
    if i in command:
      C = subprocess.run(command[5:],capture_output=True,shell=True,text=True)
      with open("Memory/Temp_Mem.txt","a",encoding="utf-8") as f:
       f.write(f"[System]:\n{C.stdout}\n")


#==============Main System==============
def WakeUp():
  print("Woke Up!")

  #============Record User's Speech=============
  threading.Thread(target=ON,daemon=True).start()
  Recording = SpeechRec.Record()


  #======STT(Transcribe Speech to Text)=========
  Speech = Transcribtion(Recording)


  #============Getting AI response==============
  Ai_Speech = Load_Model.Fetch_Respone(OpenAI_Key,"[User Input]:" + Speech,Personality)


  #===============Handle Response===============
  if "@@" in Ai_Speech:
    Speech_part,Command_part = Ai_Speech.split("@@")
    threading.Thread(target=Run_Command, args=(Command_part,)).start()
  else:
    Speech_part = Ai_Speech
  threading.Thread(target=TTS.Say(Speech_part)).start()

  #=======Saving History of Conversation(Temp Memory)=======
  with open("Memory/Temp_Mem.txt","a",encoding="utf-8") as f:
    f.write(f"[{datetime.now()}]\n[User]:{Speech}\n[Aether]:{Ai_Speech}\n")

  
  #==========Checking if Assistant should shut down===========
  if "@\@\@" not in Ai_Speech:
    WakeUp()
  else:
    threading.Thread(target=OFF,daemon=True).start()
    Summerise_memory()


#==============Save memory before shutting down==============
def Summerise_memory():
  Summery = Load_Model.Summerise(AI_Key,"""You are now presented with a conversation between an Ai assistant and the User.
                                
                                 Use The [Temp Memory] to update The [Core Memory].

                                 Make sure to save any important information from the [Temp Memory] into [Core Memory].
                                
                                Answer Format Example:

                                [2025/02/02 - 12:30 =>13:00]
                                 -User was debbuging a bug in his codebase with Ai assistant help
                                 -User took a gaming break
                                 
                                [2025/03/09 - 10:00 =>11:00]
                                 -User Watched some Youtube
                                 -User asked ordered the Ai assistant to lwoer humor level to 75%
                                 """)
  #==========Save Summery of session into memory=============
  with open("Memory/Core_Mem.txt","w",encoding="utf-8") as f: 
    f.write(Summery)
  #===================Clean Temp Memory======================
  with open("Memory/Temp_Mem.txt","w",encoding="utf-8") as f:
    f.write("")



threading.Thread(target=setup_tray,daemon=True).start()
WakeWord.start_Listening(WakeUp=WakeUp)