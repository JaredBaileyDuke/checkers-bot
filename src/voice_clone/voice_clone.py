"""
This script takes a cloned voice, and plays it over speakers on the robot
Premade audio files are available in the premade_audio folder
On the fly audio can be generated through the API call
"""

from playsound import playsound

def play_audio(audio_file):
    """
    Choose a random smackTalk audio file from the premade_audio folder and play it
    """
    # Choose a random number between 1 and 50, inclusive
    random_number = random.randint(1, 50)
    # Play the audio file
    audio_file = f"premade_audio/smackTalk_{random_number}.wav"
    playsound(audio_file)
    return

if __name__ == "__main__":
    play_audio()