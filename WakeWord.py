#===================Libraries==========================
import pvporcupine
import sounddevice as sd
import struct

por = None
def start_Listening(Access_Key,WakeUp):
  global por
  por = pvporcupine.create(access_key=Access_Key,keyword_paths=None,keywords=["computer"])

  def Listen_Wake(data,frames,time,status):
    if status:
      print(status)
    
    pcm = struct.unpack_from("h" * por.frame_length,data[:,0].tobytes())

    if por.process(pcm) >= 0:
      WakeUp()

  with sd.InputStream(
    channels=1,
    samplerate=por.sample_rate,
    blocksize=por.frame_length,
    dtype="int16",
    callback=Listen_Wake
    ):
    
    print("Listening for wake word...")
    while True:
      pass