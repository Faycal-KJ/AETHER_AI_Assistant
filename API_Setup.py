#This Script is a quick Shortcut to create a .env file with Api Keys.Just Run it in a terminal and input required Apis.


import os

# Get the absolute path to the directory where this script lives
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")

# Get user input
Key1 = input("Enter Openrouter API Key here: ")
Key2 = input("Enter Porcupine API key here: ")

# Write to .env in the script's directory
with open(env_path, "w") as f:
    f.write(f"OpenAI_Key=\"{Key1}\"\nAPI_KEY=\"{Key2}\"")
