from resemblyzer import VoiceEncoder,preprocess_wav

encodeur = VoiceEncoder()
def Recognize(Speech):
  Speech = preprocess_wav(Speech)
  embed = encodeur.embed_utterance(Speech)