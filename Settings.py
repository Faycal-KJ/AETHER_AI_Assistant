import os



def Menu():
    Option = input("""These are The settings of The AI assistant.
               enter the number of the option you want to modify:
               1. Enter API Keys
               2. Change Assistant Personality
               3. Wipe Assistant Memory
               
               Enter here:""")
    if (Option == "1"):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.join(script_dir, ".env")

        Key1 = input("Enter Openrouter API Key here: ")
        Key2 = input("Enter Porcupine API key here: ")

        with open(env_path, "w") as f:
            f.write(f"OpenAI_Key=\"{Key1}\"\nAPI_KEY=\"{Key2}\"")
        print("Keys Entered Successfuly")
        Menu()
    elif (Option == "2"):
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
    elif Option == "3":
        Confirmation = input("Are you sure you want to Delete all of assistant Memory(you can edit it in the Memory folder if you need) y/n:")
        if Confirmation == "y" or Confirmation == "Y":
            with open("Memory/Core_Memory.txt","w") as f:
                f.write("")
            print("Memory Wiped")
            Menu()
        else:
            print("Memory preserved")
            Menu()
    else:
        print("Please Pick an available option!")
        Menu()
Menu()