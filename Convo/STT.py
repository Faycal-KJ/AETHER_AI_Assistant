#=============Model=================
from faster_whisper import WhisperModel

Whisper = WhisperModel("base",compute_type="auto")


#============Transcribing audio from SpeechRec.py=============
def Transcribe(result):
  segments,_ = Whisper.transcribe(result)

  response = ''
  for segment in segments:
    response += segment.text + ""
  return response #Transcribtion of what User Said