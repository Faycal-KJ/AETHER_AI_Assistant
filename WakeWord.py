#===================Libraries==========================
import pvporcupine
import sounddevice as sd
import struct
import threading
import signal
import sys

por = None
keep_running = threading.Event()
def start_Listening(Access_Key,WakeUp):
  global por
  por = pvporcupine.create(access_key=Access_Key,keywords=["computer"])

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
    