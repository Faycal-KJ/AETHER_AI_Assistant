import mss
import requests
import base64
import json
import os

OpenAI_Key = os.getenv("OpenAI_Key")
def Screenshot():
    with mss.mss() as sct:
        img = sct.grab(sct.monitors[0])
        png_bytes = mss.tools.to_png(img.rgb, img.size)
        b64 = base64.b64encode(png_bytes).decode('utf-8')
        data_url = f"data:image/png;base64,{b64}"
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
            "Authorization": f"Bearer {OpenAI_Key}",
            "Content-Type": "application/json"
            },
            data=json.dumps({
            "model": "meta-llama/llama-4-scout",
            "messages": [
                {
                "role": "user",
                "content": [
                    {"type": "text", "text": """You are Currently the core of the vision system for an ai assistant on Desktop-PC everything you describe is used a s information by that Ai Assistant
                        Provide a Short description of what you see for the AI assistant."""},
                    {"type": "image_url", "image_url": {"url": data_url}}
                ]
                }
            ]
            })
        )
        if response.status_code == 200:
            with open("Memory/Screen_Description.txt","w",encoding="utf-8") as f: 
                f.write(response.json()["choices"][0]["message"]["content"])
        else:
            print(f" Error {response.status_code}: {response.text}")
    except requests.exceptions.JSONDecodeError:
        print("Server returned invalid JSON")