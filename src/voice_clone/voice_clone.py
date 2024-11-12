"""
This script takes a cloned voice, and plays it over speakers on the robot
Premade audio files are available in the premade_audio folder
On the fly audio can be generated through the API call
"""

import pygame
import random

def play_audio():
    """
    Choose a random smackTalk audio file from the premade_audio folder and play it
    """
    # Choose a random number between 1 and 50, inclusive
    random_number = random.randint(1, 50)
    # Play the audio file
    audio_file = f"premade_audio/smackTalk_{random_number}.mp3"

    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():  # Wait for the music to finish playing
        pass
    
    return

if __name__ == "__main__":
    play_audio()