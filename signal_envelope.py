import librosa
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

# Load the audio file
audio_file_path = 'D:/哈利波特/1哈利波特与魔法石/trimmed_audio/1_HP-12-[AudioTrimmer.com].mp3'
y, sr = librosa.load(audio_file_path)

# Compute the signal envelope using the Hilbert transform
envelope = np.abs(signal.hilbert(y))

# Calculate the threshold for detecting significant loudness changes
threshold = np.mean(envelope) + np.std(envelope)

# Calculate the mean and standard deviation of the envelope
mean_env = np.mean(envelope)
std_env = np.std(envelope)
std1 = mean_env + std_env
std2 = mean_env + 2 * std_env
std3 = mean_env + 3 * std_env

# Create the time array in seconds
time = np.arange(len(y)) / sr

# Calculate the mean and standard deviation of the signal envelope every 0.5 seconds
window_size = int(0.5 * sr)
envelope_mean = []
envelope_std = []
for i in range(0, len(y) - window_size, window_size):
    envelope_mean.append(np.mean(envelope[i:i+window_size]))
    envelope_std.append(np.std(envelope[i:i+window_size]))

# Create the time array for the mean and standard deviation plot
time_mean_std = np.arange(len(envelope_mean)) * window_size / sr + window_size / (2 * sr)

# Plot the signal, envelope, and mean and standard deviation
fig, axs = plt.subplots(nrows=3, sharex=True, figsize=(12, 12))
axs[0].plot(time, y, alpha=0.5)
axs[0].set(title='Original signal')
axs[0].set_ylabel('Amplitude')
title_pos = axs[0].title.get_position()
axs[0].title.set_position([title_pos[0], 1.05])
axs[1].plot(time, envelope, color='r', alpha=0.5)
axs[1].axhline(threshold, color='k', linestyle='--', linewidth=1)
axs[1].set(title='Signal envelope')
axs[1].set_ylabel('Amplitude envelope')
title_pos = axs[1].title.get_position()
axs[1].title.set_position([title_pos[0], 1.05])
axs[2].plot(time_mean_std, envelope_mean, color='r', alpha=0.5)
axs[2].fill_between(time_mean_std, np.array(envelope_mean) + np.array(envelope_std), np.array(envelope_mean) - np.array(envelope_std), alpha=0.2)
axs[2].set(title='Mean and standard deviation of signal envelope')
axs[2].set_xlabel('Time (seconds)')
axs[2].set_ylabel('Amplitude envelope')
title_pos = axs[2].title.get_position()
axs[2].title.set_position([title_pos[0], 1.05])
plt.subplots_adjust(hspace=0.5)
plt.show()

# Calculate and print the compression threshold in decibels
compression_threshold_db = 20 * np.log10(threshold / mean_env)
print(f"Compression threshold: {compression_threshold_db:.2f} dB")

print(f"1st std: {std1:.2f}")
print(f"2nd std: {std2:.2f}")
print(f"3rd std: {std3:.2f}")
