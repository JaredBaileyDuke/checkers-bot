import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import speech_recognition as sr
def record_audio(file_name, seconds):
    """
    Record audio for a specified duration and save it to a file.
    Args:
        file_name (str): The name of the file to save the audio.
        seconds (int): The duration in seconds to record audio.
    Returns:
        Boolean: True if the audio was successfully recorded and saved.
    """
    fs = 44100  # Sample rate
    duration = seconds  # seconds
    # Record the audio using sounddevice
    print("Recording...")
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    print("Recording finished.")
    # Save the recording as a WAV file
    write(file_name, fs, myrecording)
    print(f"Recording saved to {file_name}")
    return True
def speech_to_text(file_name):
    """
    Convert speech from an audio file to text.
    Args:
        file_name (str): The name of the audio file to convert to text.
    Returns:
        str: The text converted from speech.
    """
    # Load the saved .wav file and recognize speech
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_name) as source:
        audio = recognizer.record(source)
    try:
        # Use Google's speech recognition to convert the audio to text
        print("Recognizing speech...")
        text = recognizer.recognize_google(audio)
        text = text.lower()
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None
if __name__ == "__main__":
    # Record audio for 5 seconds
    audio_file = "sample_audio.wav"
    record_audio(audio_file, 5)
    # Convert speech to text
    text = speech_to_text(audio_file)
    print(text)







