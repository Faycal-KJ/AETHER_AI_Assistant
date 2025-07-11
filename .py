import random
import os
#===========Libraries============
import subprocess
import soundfile as sf
import sounddevice as sd



#=============Paths=============
piper_path = ".\\piper\\piper.exe"
model_path = ".\\piper\\voices\\en_US-ryan-low.onnx"
config_path = ".\\piper\\voices\\en_US-ryan-low.onnx.json"



sentence_silence = "0.5"


#==========Generating Audio From Assistant Response(Speech to Text)===============
def Say():
  #===========Running Piper===============
  TTS = subprocess.Popen(
    [
      piper_path,
      "--model",model_path,
      "--config",config_path,
      "--output_file","AI_Says.wav",
      "--sentence_silence",sentence_silence,
    ],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
  )

  data, sample_rate = sf.read(f"Startup_SYS/WakeResponses/Call_response{random.randrange(1,17)}.wav")
  sd.play(data,sample_rate)
  sd.wait()
Say()