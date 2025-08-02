#=========Libraires===============
import sys
import threading
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image
from pystray import Icon,Menu,MenuItem
import System_Info.System as System
import time
import re
import os
#========Helper Scripts=============
import Convo.STT as STT
import Convo.TTS as TTS
import Startup_SYS.WakeWord as WakeWord
import Model.Load_Model as Load_Model
import Convo.SpeechRec as SpeechRec

#===============Assets/Configurators===============
AI_ON_Image = Image.open("Assets/ON.png")
AI_OFF_Image = Image.open("Assets/OFF.png")
Personality = open("Personalities/Current_Personality.txt","r",encoding="utf-8").read()
Temp_Mem_File = open("Memory/Temp_Mem.txt", "a", encoding="utf-8", buffering=1)
CMD_WHITELIST = set([
        # System Info
    "systeminfo",
    "hostname",
    "whoami",
    "ver",
    "wmic",
    "wmic cpu get name",
    "wmic os get Caption",
    "powershell Get-ComputerInfo",
    "powershell Get-CimInstance Win32_Processor",
    "powershell Get-CimInstance Win32_LogicalDisk",
    "powershell Get-CimInstance Win32_OperatingSystem",
    "net stats workstation",

    # Task & Process Management
    "tasklist",
    "taskmgr",
    "resmon",
    "perfmon",
    "powershell Get-Process",
    "powershell Get-Process | Sort-Object CPU -Descending | Select-Object -First 10",
    "powershell Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 10",
    "kill",                       # Custom kill command logic
    "start",                      # Start applications

    # Network Diagnostics
    "ping",
    "ipconfig",
    "ipconfig /all",
    "netstat -e",
    "tracert www.google.com",
    "powershell Test-NetConnection google.com",
    "arp -a",
    "nslookup google.com",
    "netsh wlan show interfaces",
    "netsh interface ipv4 show config",

    # Services
    "powershell Get-Service",
    "powershell Get-Service | Where-Object {$_.Status -eq 'Running'}",

    # Environment & File Navigation
    "dir",
    "cd",
    "findstr",
    "set",
    "echo",
    "cls",

    # Time/Date Utilities
    "date /T",
    "time /T",

    # Hardware & USB
    "wmic logicaldisk get name,size,freespace,volumename",
    "fsutil volume diskfree c:",
    "powershell Get-PnpDevice -Class DiskDrive",
    "powershell Get-WmiObject Win32_USBControllerDevice",

    # User Session & Groups
    "query user",
    "whoami /groups",
    "whoami /priv",
    "net user",

    # Scheduled Tasks
    "schtasks /query /fo LIST /v",

    # Installed Programs
    "powershell Get-WmiObject -Class Win32_Product",

    # Firewall & Security
    "netsh advfirewall show allprofiles",

    # Battery Reports (Laptop)
    "powercfg /batteryreport",
    "powercfg /energy",

    # Tools
    "speedtest-cli",
    "shutdown"
])
load_dotenv("_internal/.env")
load_dotenv("_internal/Set.env")
Type = os.getenv("Conv")
#============Toolbar Icon==============
def quit_app(icon, item):
    Summerise_memory()
    sys.exit(0)
    WakeWord.keep_running.set()
    print("Turning OFF Assistant")
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

def Sys_info():
  while True:
    System.Fetch()
    time.sleep(1)
#==========Run AI cammands===============
def Run_Command(command):
  for i in CMD_WHITELIST:
    if i in command:
      C = subprocess.run(command,capture_output=True,shell=True,text=True)
      with open("Memory/Temp_Mem.txt","a",encoding="utf-8") as f:
       f.write(f"[System]:\n{C.stdout}\n")
#==============Main System==============
def WakeUp():
  if Type == "1":
    Speech = input("User: ")
  if Type == "2":
    #============Record User's Speech=============
    threading.Thread(target=ON,daemon=True).start()


    Record = SpeechRec.Record()

    Speech = STT.Transcribe(Record)
  if Speech == "/Z":
    Summerise_memory()
    os._exit(0)
  #============Getting AI response==============
  Ai_Speech = Load_Model.Fetch_Respone("[User Input]:" + Speech,Personality)
  if Ai_Speech:
    Ai_Speech = Ai_Speech.replace("*","...",Ai_Speech.count("*"))
  #===============Handle Response===============
  if "CMD:" in Ai_Speech:
      matches = re.split(r"CMD:", Ai_Speech)
    
        # First part is speech, rest are command blocks
      Speech_part = matches[0].strip()
      
      # Each other part might contain one or multiple commands
      for command_block in matches[1:]:
          # Split block into individual commands (in case it's multi-line)
          commands = command_block.strip().splitlines()
          
          for command in commands:
              command = command.strip()
              if command:
                  threading.Thread(target=Run_Command, args=(command,)).start()
  else:
    Speech_part = Ai_Speech
  if "@_@_@" in Speech_part:
    Speech_part,A = Speech_part.split("@_@_@")
  T1 = threading.Thread(target=TTS.Say, args=(Speech_part,None))
  print("Assistant:",Speech_part)
  T1.start()
  #=======Saving History of Conversation(Temp Memory)=======
  Temp_Mem_File.write(f"[{datetime.now()}]\n[User]:{Speech}\n[Aether]:{Ai_Speech}\n")

  #==========Checking if Assistant should shut down===========
  T1.join()
  if "@_@_@" not in Ai_Speech:
    WakeUp()
  else:
    if Type == "2":
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
if Type == "2":
  threading.Thread(target=setup_tray,daemon=True).start()
  WakeWord.start_Listening(WakeUp=WakeUp)

threading.Thread(target=Sys_info).start()
if Type == "1":
  WakeUp()
