import pyttsx3

engine = pyttsx3.init()

engine.setProperty('rate', 150)     # speech speed
engine.setProperty('volume', 1.0)   # max volume

engine.save_to_file("TRUST THE MALWARE", "cleanform.wav")
engine.runAndWait()

print("cleanform.wav created.")

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

# Load clean audio
rate, data = wavfile.read("cleanform.wav")

# Convert to float
data = data.astype(np.float32)

# Add heavy white noise
noise = np.random.normal(0, 3000, data.shape)
noisy = data + noise

# Apply bandpass filter (distortion effect)
def bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

b, a = bandpass(300, 1500, rate)
filtered = lfilter(b, a, noisy)

# Add clipping distortion
distorted = np.clip(filtered * 2, -20000, 20000)

# Convert back to int16
distorted = distorted.astype(np.int16)

# Save
wavfile.write("distorted.wav", rate, distorted)

print("distorted.wav created.")
