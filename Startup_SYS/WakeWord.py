#===================Libraries==========================
import pvporcupine
import sounddevice as sd
import threading
import struct
import os
from dotenv import load_dotenv
load_dotenv()


Access_Key = os.getenv("API_KEY")
keep_running = threading.Event()
#==============Fetching WakeWord Model===============
por = pvporcupine.create(access_key=Access_Key,keywords=["computer"])
def start_Listening(WakeUp):

  #===========Waiting For WakeWord=================
  def Listen_Wake(data,frames,time,status):
    if status:
      print(status)
    
    pcm = struct.unpack_from("h" * por.frame_length,data[:,0].tobytes())

    
    if por.process(pcm) >= 0:
      WakeUp()#Firing main function

  with sd.InputStream(
    channels=1,
    samplerate=por.sample_rate,
    blocksize=por.frame_length,
    dtype="int16",
    callback=Listen_Wake
    ):
    
    print("Listening for wake word...")
    keep_running.wait()
    