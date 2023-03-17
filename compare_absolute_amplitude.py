from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt

# Load original audio file
orig_audio = AudioSegment.from_file('audio_files/1_HP-01-[AudioTrimmer.com].mp3', format='mp3')
orig_audio_array = np.array(orig_audio.get_array_of_samples())

# Load cleaned audio file
clean_audio = AudioSegment.from_file('audio_files/1_HP-01-[AudioTrimmer.com]_cleaned.mp3', format='mp3')
clean_audio_array = np.array(clean_audio.get_array_of_samples())

# Calculate maximum absolute amplitude of both files
orig_max_amplitude = 20 * np.log10(np.max(np.abs(orig_audio_array)))
clean_max_amplitude = 20 * np.log10(np.max(np.abs(clean_audio_array)))

# Plot the maximum absolute amplitude comparison
fig, axs = plt.subplots(2, 1, figsize=(8,8))
axs[0].bar(['Original', 'Cleaned'], [-orig_max_amplitude, -clean_max_amplitude])
axs[0].set_xlabel('Audio File')
axs[0].set_ylabel('Maximum Absolute Amplitude (dBFS)')
axs[0].set_title('Maximum Absolute Amplitude Comparison')

# Plot the noise profile comparison
orig_noise_profile, orig_freqs = plt.psd(orig_audio_array, Fs=orig_audio.frame_rate)
clean_noise_profile, clean_freqs = plt.psd(clean_audio_array, Fs=clean_audio.frame_rate)

axs[1].semilogx(orig_freqs, 10*np.log10(orig_noise_profile), label='Original')
axs[1].semilogx(clean_freqs, 10*np.log10(clean_noise_profile), label='Cleaned')
axs[1].set_xlabel('Frequency (Hz)')
axs[1].set_ylabel('Power/Frequency (dB/Hz)')
axs[1].set_title('Noise Profile Comparison')
axs[1].legend()

plt.tight_layout()
plt.show()
