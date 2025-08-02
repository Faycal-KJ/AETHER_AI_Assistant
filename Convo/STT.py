#=============Model=================
from faster_whisper import WhisperModel

Whisper = WhisperModel("tiny",compute_type="auto")


#============Transcribing audio from SpeechRec.py=============
def Transcribe(result):
  segments,_ = Whisper.transcribe(result,beam_size=1,word_timestamps=False)
  response = ''
  for segment in segments:
    response += segment.text + ""
  return response #Transcribtion of what User Said