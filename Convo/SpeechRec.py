import soundfile as sf
import sounddevice as sd
import numpy as np
import io

def Record():
  sample_rate = 16000
  block_duration = 0.1
  channels = 1
  silence_threshold = 150
  speaking_threshold = 400
  silence_duration = 1

  block_size = int(block_duration * sample_rate)
  req_silence = int(silence_duration / block_duration)

  isTalking = False
  buffer = []
  silence_count = 0

  stream = sd.InputStream(samplerate=sample_rate,blocksize=block_size,channels=channels,dtype='int16')
  with stream:
    while True:
      block,_ = stream.read(block_size)
      buffer.append(block)

      RMS = np.sqrt(np.mean(np.square(block.astype('float32'))))

      print(RMS)
      if not isTalking and RMS > speaking_threshold:
          isTalking = True
          print("Voice detected, started recording...")

      if isTalking:
          if RMS < silence_threshold:
              silence_count += 1
          else:
              silence_count = 0
          if silence_count >= req_silence:
                    print("Done Listening")
                    break
  result = np.concatenate(buffer,axis=0)
  buffer = io.BytesIO()
  sf.write(buffer,result,sample_rate,format="WAV")
  buffer.seek(0)
  return buffer