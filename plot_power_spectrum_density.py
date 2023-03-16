import numpy as np
import scipy.signal as signal
import librosa.display
import matplotlib.pyplot as plt

# Load the audio file
audio_data, sample_rate = librosa.load('D:/哈利波特/1哈利波特与魔法石/trimmed_audio/1_HP-01-[AudioTrimmer.com].mp3', sr=None)

# Calculate the power spectral density (PSD)
frequencies, psd = signal.welch(audio_data, fs=sample_rate)

# Plot the PSD
plt.figure(figsize=(10, 4))
plt.semilogx(frequencies, 10 * np.log10(psd))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power/Frequency (dB/Hz)')
plt.title('Power Spectral Density')

# Set the x-axis ticks and labels
xticks = [20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
xticklabels = [str(x) for x in xticks]
plt.xticks(xticks, xticklabels)

plt.show()
