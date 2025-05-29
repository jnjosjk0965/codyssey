import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import os
from datetime import datetime

def record_audio(duration=10, fs=44100):
    """
    Records audio from the microphone for a specified duration and saves it.

    Args:
        duration (int): The duration of the recording in seconds.
        fs (int): The sample rate (samples per second).
    """
    # Create 'records' directory if it doesn't exist
    if not os.path.exists("records"):
        os.makedirs("records")

    print(f"Recording for {duration} seconds...")

    try:
        # Record audio
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()  # Wait until recording is finished

        # Generate filename with current date and time
        now = datetime.now()
        filename = now.strftime("%Y%m%d-%H%M%S.wav")
        filepath = os.path.join("records", filename)

        # Save the recorded audio
        write(filepath, fs, myrecording)
        print(f"Recording saved to {filepath}")

    except Exception as e:
        print(f"An error occurred during recording: {e}")

if __name__ == "__main__":
    # You can change the duration here (e.g., record for 10 seconds)
    record_audio(duration=5)