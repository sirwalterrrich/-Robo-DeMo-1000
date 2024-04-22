#!/usr/bin/env python
# Author : Sir Walter R. April 20, 2024
# Script Title - motivator_demotivator_1000.py
# This script uses the ElevenLabs AI voice service to generate speech from text.
# The text come from lists(motivations, demotivations, motivations2 ) of AI generated phrases (chatGPT)
# that would either motivate or demotivate a distance runner.
# Once executed, the messaging is at random. A random message from the list will be selected to be played. 
# The script saves the audio file as output.mp3

# Future work: I hope to use Computer Vision facial recognition models to trigger the type of selected messages.
# For example, if the person looks super stressed during a run then tell them something motivational or funny.
# Future work: Save the output.mp3 files for later use to save on bandwidth and ElevenLabs API Usage.

# This script uses the ElevenLabs API for speech to text generation and pygame libraries for audio output.
 
import pygame
import random
from elevenlabs.client import ElevenLabs, Voice, VoiceSettings

# Initialize pygame mixer
pygame.mixer.init()

# Instantiate the client with your API key. You'll need to goto ElevenLabs to set up an account for API access
client = ElevenLabs(api_key="Insert API KEY HERE")

# Specify the voice settings with the desired voice ID # Bella
voice_id = "EXAVITQu4vr4xnSDxMaL" # Bella You'll need to go to ElevenLabs to get the full list of available voices

# List of motivational and demotivational messages
motivations = [
    "Push through, victory awaits ahead.",
    "Step by step, reach beyond.",
    "Embrace the challenge, defy limits.",
    "Fuel your stride, conquer distances.",
    "Every mile, a step closer.",
    "Find strength in each stride.",
    "Run your path, own it.",
    "Mind over miles, you soar.",
    "Break barriers, chase dreams relentlessly.",
    "With every breath, redefine limits."
]

demotivations = [
    "You'll never reach the finish.",
    "Why bother? You'll fail anyway.",
    "Too slow, give up now.",
    "Not good enough, quit running.",
    "Pain is your only reward.",
    "You're not built for running.",
    "Miles ahead, you'll still lag.",
    "Running won't change a thing.",
    "Your efforts won't matter.",
    "Just stop, it's pointless."
]

motivations2 = [
    "Stride strong, you’ve got this!",
    "Keep pushing, every step counts!",
    "Go for it, runner’s high awaits!",
    "Chase the pace, feel the breeze!",
    "Run with heart, shine with sweat!",
    "Embrace the run, enjoy the journey!",
    "Speed thrills, keep the rhythm!",
    "Your race, your pace, your triumph!",
    "Legs on fire, spirit inspired!",
    "Pound the path, own the moment!"
]

# Combine both lists and select a random message
messages = motivations + demotivations + motivations2
selected_message = random.choice(messages)
print("Message: " + selected_message)

# Customize voice settings
voice_settings = VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)

# Generate audio from the selected text
audio_generator = client.generate(text=selected_message, voice_settings=voice_settings)

# Consume the generator to get the bytes-like object
audio_bytes = b"".join(audio_generator)

# Save the audio to a file
audio_file = "output.mp3"
with open(audio_file, "wb") as f:
    f.write(audio_bytes)

# Load and play the audio file
pygame.mixer.music.load(audio_file)
pygame.mixer.music.play()

# Keep the script running until the audio is done playing
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
