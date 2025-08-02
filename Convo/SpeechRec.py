#=======Libraries===========
import soundfile as sf
import sounddevice as sd
import numpy as np
import io
import os
from dotenv import load_dotenv
load_dotenv("Set.env")


#=========Record Mic Input==========
def Record():
  
    #========configurators===========
    sample_rate = 16000
    block_duration = 0.1
    channels = 1
    silence_threshold = os.getenv("silence")
    speaking_threshold = os.getenv("Voice")
    silence_duration = 1
    block_size = int(block_duration * sample_rate)
    req_silence = int(silence_duration / block_duration)
    isTalking = False
    buffer = []
    silence_count = 0


    #=======Initiate MIC input Stream========
    stream = sd.InputStream(samplerate=sample_rate,blocksize=block_size,channels=channels,dtype='int16')


    with stream:
        while True:

            block,_ = stream.read(block_size)
            buffer.append(block)

            RMS = np.sqrt(np.mean(np.square(block.astype('float32'))))

            print(RMS)

            #============Detecting When User Starts to Speak==========
            if not isTalking and RMS > float(speaking_threshold):
                isTalking = True
                print("Voice detected, started recording...")

            

            #============Detecting Silence to end Recording===========
            if isTalking:
                if RMS < float(silence_threshold):
                    silence_count += 1
                else:
                    silence_count = 0
                if silence_count >= req_silence:
                        print("Done Listening")
                        break
                
    #===========Formatting Audio For Transcribtion(Whisper)==========
    result = np.concatenate(buffer,axis=0)
    buffer = io.BytesIO()
    sf.write(buffer,result,sample_rate,format="WAV")
    buffer.seek(0)
    return buffer