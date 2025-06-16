import pvporcupine
import sounddevice as sd
import struct

Access_Key = 'MmqrmxmKlkDsuoedTyztiOUxdmMIUQIkjQYdllQ1SKcsJAcFH+RBqw=='


def WakeUp():
  print("Assistant Awake!")

por = pvporcupine.create(access_key=Access_Key,keyword_paths=None,keywords=["computer"])

def Listen_Wake(data,frames,time,status):
  if status:
    print(status)
  
  pcm = struct.unpack_from("h" * por.frame_length,data[:,0].tobytes())

  result = por.process(pcm)
  if result >= 0:
    WakeUp()

with sd.InputStream(channels=1,samplerate=por.sample_rate,blocksize=por.frame_length,dtype="int16",callback=Listen_Wake):
  print("Listening for wake word...")
  while True:
    pass