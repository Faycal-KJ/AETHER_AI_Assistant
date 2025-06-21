from faster_whisper import WhisperModel

Whisper = WhisperModel("tiny",compute_type="auto")
def Transcribe(result):
  segments,_ = Whisper.transcribe(result)

  response = ''
  for segment in segments:
    response += segment.text + ""
  return response