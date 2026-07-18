from gtts import gTTS
import pygame

text = "Hello! I am Sofi."

tts = gTTS(text=text, lang="en")
tts.save("voice.mp3")

pygame.mixer.init()
pygame.mixer.music.load("voice.mp3")
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pass