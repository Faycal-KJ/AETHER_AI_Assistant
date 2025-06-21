#===================Libraries==========================
import pvporcupine
import sounddevice as sd
import numpy as np
import threading
import signal
import struct
import sys
import os
from dotenv import load_dotenv

load_dotenv()
Access_Key = os.getenv("API_KEY")

por = None
keep_running = threading.Event()
por = pvporcupine.create(access_key=Access_Key,keywords=["computer"])
def start_Listening(WakeUp):

  def Listen_Wake(data,frames,time,status):
    if status:
      print(status)
    
    pcm = struct.unpack_from("h" * por.frame_length,data[:,0].tobytes())

    if por.process(pcm) >= 0:
      WakeUp()

  def Exit(sig,frame):
    keep_running.set()
    por.delete()
    sys.exit(0)

  signal.signal(signal.SIGINT,Exit)

  with sd.InputStream(
    channels=1,
    samplerate=por.sample_rate,
    blocksize=por.frame_length,
    dtype="int16",
    callback=Listen_Wake
    ):
    
    print("Listening for wake word...")
    keep_running.wait()
    