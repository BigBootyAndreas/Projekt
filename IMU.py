import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Step 1: Generate a synthetic signal (e.g., a sine wave with added noise)
fs = 1000  # Sampling frequency in Hz
duration = 2  # Duration in seconds
t = np.linspace(0, duration, fs * duration, endpoint=False)  # Time vector

# Create a signal: a 50 Hz sine wave with added Gaussian noise
signal_data = np.sin(2 * np.pi * 50 * t) + 0.5 * np.random.randn(len(t))

# Step 2: Compute the PSD using Welch's method
frequencies, psd = signal.welch(signal_data, fs, nperseg=1024)

# Step 3: Plot the PSD
plt.figure(figsize=(10, 6))
plt.semilogy(frequencies, psd)
plt.title('Power Spectral Density (PSD)')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Power/Frequency [dB/Hz]')
plt.grid()
plt.show()
