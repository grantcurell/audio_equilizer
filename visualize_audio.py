import librosa
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

try:
    import PyQt6
    import PySide2
except ImportError:
    print("Error: PyQt6 or PySide2 module not found.")
    print("Please make sure both modules are installed before running this program.")
    exit()

matplotlib.use('Qt5Agg')

# Load the audio file into a numpy array
audio_data, sample_rate = librosa.load('D:/哈利波特/1哈利波特与魔法石/trimmed_audio/1_HP-01-[AudioTrimmer.com].mp3')

# Print the bit depth
print(f"Bit depth: {audio_data.dtype.itemsize * 8}")

time_values = np.linspace(0, len(audio_data)/sample_rate, num=len(audio_data))

# Calculate the RMS of the audio signal using a sliding window
window_size = 0.1
window_length = int(window_size * sample_rate)
rms_values = np.sqrt(np.convolve(audio_data**2, np.ones(window_length)/window_length, mode='valid'))

# Calculate the dBFS level of the audio signal
dbfs = 20 * np.log10(np.max(np.abs(audio_data)))

# Calculate the Fourier Transform of the audio signal
audio_fft = np.fft.fft(audio_data)

# Calculate the power spectral density
power_spectral_density = np.abs(audio_fft)**2

# Calculate the frequency axis
frequency_axis = np.fft.fftfreq(len(audio_data), 1/sample_rate)

# Create a 4x1 subplot grid and plot the waveform, RMS plot, dBFS plot, and frequency domain plot
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 20), sharex=False, gridspec_kw={'hspace': 0.5})
fig.suptitle('Audio Visualization', fontsize=16)

# Plot the waveform
ax1.plot(time_values, audio_data)
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Amplitude')
ax1.set_title('Waveform')

# Plot the RMS values over time
time_values_rms = np.linspace(0, len(audio_data)/sample_rate, num=len(rms_values))
ax2.plot(time_values_rms, rms_values)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('RMS Amplitude')
ax2.set_title('Loudness')

ax3.plot(time_values, 20 * np.log10(np.abs(audio_data)), color='blue')
ax3.axhline(y=-1, color='red', linestyle='--', alpha=1, zorder=4, label='Professional-level audio (-1 dBFS)')
ax3.axhline(y=-16, color='yellow', linestyle='--', alpha=1, zorder=3, label='Consumer-level audio (-16 dBFS)')
ax3.axhline(y=-24, color='magenta', linestyle='--', alpha=1, zorder=2, label='TV and radio broadcasting (-24 dBFS)')
ax3.plot([0, len(audio_data)/sample_rate], [dbfs, dbfs], linestyle='--', color='purple', zorder=1,
         label='Maximum dBFS level reached')
ax3.set_ylim([-60, 0])
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('dBFS')
ax3.set_title('Volume Level')
ax3.legend(bbox_to_anchor=(0., -0.3, 1., .102), loc='lower left', ncol=2, mode="expand", borderaxespad=0.)

# Plot the power spectral density in the frequency domain
ax4.plot(frequency_axis[:len(frequency_axis)//2], 10 * np.log10(power_spectral_density[:len(power_spectral_density)//2]))
ax4.set_xlabel('Frequency (Hz)')
ax4.set_ylabel('Power (dB)')
ax4.set_title('Frequency Domain')

# Show the plot
plt.show()

