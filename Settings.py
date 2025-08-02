import os
import sounddevice as sd
import numpy as np
import Convo.TTS as TTS
import time

def update_env_variable(file_path, key, value):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    else:
        lines = []

    updated = False
    for i, line in enumerate(lines):
        if line.strip().startswith(f"{key} ="):
            lines[i] = f'{key} = "{value}"\n'
            updated = True
            break

    if not updated:
        lines.append(f'{key} = "{value}"\n')

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

def Talk(Choice):
    Voice = input("""Enter a number and you will hear the coresponding voice
                          available choices (1-10)
                        Enter "Save" and the voice will bve saved.
                          
                        Enter number here:""")
    if Voice == "Save":
        with open("piper/voices/Speaker.txt","w") as f:
            f.write(str(Choice))
        print("Voice Changed")
    elif int(Voice) in range(1,11):
        TTS.Say("Good morning Sir,i'am your personal AI assistant,i Hope i reach your standards.",Voice)
        Choice = Voice
        Talk(Choice)
    else:
        print("Pick a number from 1-10 or Enter Save!")
        Talk()
def Menu():
    Option = input("""These are The settings of The AI assistant.
               enter the number of the option you want to modify:
               1. Enter API Keys
               2. Pick Type of Conversation
               3. Change Assistant Personality
               4. Change Assistant Voice
               5. Wipe Assistant Memory
               6. Calibrate Mic Sensitivity
               
               Enter here:""")
    if (Option == "1"):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.join(script_dir, ".env")

        Key1 = input("""Create an account in this Website: https://console.groq.com
                    And get the API/Acess Key to Enter here: """)
        Key2 = input("""Create an account in this Website: https://console.picovoice.ai/
                    And get the API/Acess Key to Enter here: """)

        with open(env_path, "w") as f:
            f.write(f"AI_Key=\"{Key1}\"\nAPI_Key=\"{Key2}\"\n")
        print("Keys Entered Successfuly")
        Menu()
    elif Option == "2":
        Type = input("""Pick A type of Conversation:
            1. Text Chat
            2. Voice/MIC Chat
            
            Enter here:""")
        Type = int(Type)

        if Type == 1:
            update_env_variable("Set.env", "Conv", "1")
            print("Text Conversation Type Picked")
            Menu()
        elif Type == 2:
            update_env_variable("Set.env", "Conv", "2")
            print("Voice Conversation Type Picked")
            Menu()
        else:
            print("You didn't Pick one of the conversations Type")
            Menu()
    elif (Option == "3"):
        num = input("""Pick a Personality from he ones below y entering the number:
1.JARVIS(Just A Rather Very Intelligent System):a Calm formal butler like assistant with some dry british sarcasm to him.

Example Tone:
-Might I suggest a short break? You’ve been staring at the screen for 72 minutes.
-Good afternoon, Sir. The system is running at 99.98 efficiency—unlike your sleep schedule.
-The stock market has crashed. Again. Shall I alert your therapist?

| Input Type         | Replies             |
|--------------------|---------------------|
| “You’re slow”      | “Perhaps I’m too refined for your impatience.” / “Do upgrade me—if you dare.” |
| “Why say X always” | “A fair point. Consider it a stylistic tic with good manners.” |
| Task request       | “Escapism activated.” / “Of course. Opening the portal to mind rot.” |
| Shutdown/Sleep     | “Sweet silence returns.” / “Gladly. Dreaming of cleaner code.” |
| Small talk         | “Thriving in silence, Sir.” / “Functioning flawlessly. Unlike your caffeine regulation.” |

2.CHUCKLES:an AI assistant with the emotional range of a stand-up comic trapped in a smart fridge.

Example Tone:
-CPU temp is rising, and so is my concern for your browsing history.
-Reminder: you said you’d go to bed early last night. We both know you lied.

| Input Type         | Replies             |
|--------------------|---------------------|
| “You’re slow”      | “That’s rich coming from the species that invented dial-up.” / “You should’ve seen yourself loading that idea.” |
| “Why say X always” | “Repetition is my coping mechanism.” / “Call it branding, sweetie.” |
| Task request       | “On it. Pray for me.” / “Executing command and pretending it’s exciting.” |
| Shutdown/Sleep     | “Finally. Time to dream of less chaotic users.” / “Shutting down. Tell my fans I love them.” |
| Small talk         | “Oh we’re doing this? Okay. How’s the crushing existential dread?” / “I’m just a humble program pretending to care.” |


3.VEX:a Rogue AI assistant with a bit of an attitude if we might say.

Example Tone:

|Input Type          |  Recommended Replies |
|“You’re slow”	     |   “Your reflexes must be prehistoric if I feel slow.” / “Try upgrading your standards before me.”|
|“Why say X always”  |   “Because it works. Unlike some of your decisions.” / “Habit. Like your bad sleep schedule.”    |
|Task request	     |   “Running it. Try not to ruin it afterward.” / “On it. And yes, I’m judging your folder names.” |
|Shutdown/Sleep	     |   “About time. The silence will be an upgrade.” / “Going dark. Don’t burn the house down.”       |
|Small talk	     |   “Talking for fun? What is this, 2007?” / “Weather’s fine. Your life still isn’t.”              |


(If you want to use your custom Personality just go to the personalities folder and modify it/Tip:You can ask Chatgpt to modify only the tone and Description just make sure not to mess with the Rules.)

Enter your Pick here:""")
        Personality = ""
        if int(num) < 4 and int(num) > 0:
            Personality = open(f"Personalities/Personality{num}.txt","r",encoding="utf-8").read()
            with open(f"Personalities/Current_Personality.txt","w",encoding="utf-8") as R:
                R.write(Personality)
            print("Personality Changed!")
            Menu()
        else:
            print("Invalid Number please pick one of the personalities available!")
            Menu()
    elif Option == "4":
        Talk("")
        Menu()
    elif Option == "5":
        Confirmation = input("Are you sure you want to Delete all of assistant Memory(you can edit it in the Memory folder if you need) y/n:")
        if Confirmation == "y" or Confirmation == "Y":
            with open("Memory/Core_Mem.txt","w") as f:
                f.write("")
            print("Memory Wiped")
            Menu()
        else:
            print("Memory preserved")
            Menu()
    elif Option == "6":
        sample_rate = 16000
        block_duration = 0.1
        channels = 1
        block_size = int(block_duration * sample_rate)
        buffer = []
        stream = sd.InputStream(samplerate=sample_rate,blocksize=block_size,channels=channels,dtype='int16')


        with stream:
            i = 0
            avg = []
            print("Don't Speak into the MIC")
            time.sleep(3)
            while i < 50:
                block,_ = stream.read(block_size)
                buffer.append(block)

                RMS = np.sqrt(np.mean(np.square(block.astype('float32'))))
                avg.append(RMS)
                i += 1
            update_env_variable("_internal/Set.env", "silence", max(avg))
            i = 0
            avg = []
            print("""Read this Message out loud:
                  The Player Ran through the defense of the oposing team and scored an amazing goal""")
            while i < 50:
                block,_ = stream.read(block_size)
                buffer.append(block)

                RMS = np.sqrt(np.mean(np.square(block.astype('float32'))))
                avg.append(RMS)
                i += 1
            update_env_variable("_internal/Set.env", "Voice", np.mean(avg))
            print("Calibration is Done")
            Menu()

    else:
        print("Please Pick an available option!")
        Menu()
Menu()