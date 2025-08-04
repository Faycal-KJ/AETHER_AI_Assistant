
# 🤖 AETHER — Personal AI Assistant

AETHER is a voice-activated, intelligent personal assistant designed for local desktop use. It serves as a command-line and voice interface to control PC/laptop, manage files, hold natural conversations, remember user context, and assist with daily productivity tasks — all with a unique personality inspired by JARVIS.

## 🧠 Features

- **Voice Wake Word Detection**
  - Listens in the background and activates on your Trigger Word (cuurently only "Computer")

- **Natural Language Understanding**
  - NLP-powered responses with customizable personality + based tone shifting.

- **Memory Management**
  - Remembers past conversations, user preferences, moods, routines, and task history.

- **File & System Interaction**
  - Can open apps, run scripts, navigate directories, and edit files via command line.

- **Modular Plugin Support**
  - Easily extendable for web scraping, calendar syncing, task automation, etc.

## 🏗️ Tech Stack

| Component        | Technology            |
|------------------|------------------------|
| Language         | Python                 |
| NLP Model        | llama-3.3-70b-versatile (Via API)|
| Voice I/O        | `whisper`,`Piper` |
| Wake Word        | `Porcupine`|
| Memory Storage   | customizable Txt File|
| Deployment       | Background Process|

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Faycal/AETHER_AI_Assistant.git
cd aether-ai-assistant
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Setup/Customization (Optional)

```bash
python settings.py
```

### 4. Run AETHER

```bash
python main.py
```

## 🔒 Privacy:

- Conversations and voice data are stored **locally**.
- Currently There isn't a full Offline mode(But is planned to be added later)

## 🛠️ Roadmap

- [x] Wake word detection
- [x] Voice Conversation
- [x] Local memory DB
- [x] Task Excution/Commands Excution
- [x] Customizable Personality
- [x] light weight
- [ ] GUI dashboard
- [ ] Voice recognition/Profiles (Detect which user is talking)
- [ ] Emotion-aware responses (voice tone detection)
- [ ] Remote access via mobile
- [ ] Customizable Wake Word
- [ ] Plug in features(Weather.py,Calender.py...etc)
- [ ] Personality to user assigning (User1:Sarcastic,User2:Polite + Serious,..etc)

## 🤝 Issues

Please open an issue and explain your Issue.  
I will try my best to fix issues in the nearest Date.

---

## 📜 License

MIT License. See `LICENSE` file for details.

---

## 🙋‍♂️ Author

**Faisal Kdj**  
Connect with me on [LinkedIn](https://www.linkedin.com/in/kaddour-djebbar-faycal-41452327a/)  
Visit [My Portfolio Website](https://portfolio-website-c144zdbz3-faisals-projects-a393ca68.vercel.app/)
