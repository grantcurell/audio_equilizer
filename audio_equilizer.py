import librosa
import soundfile as sf

# Load the audio file
audio_data, sample_rate = librosa.load('D:/哈利波特/1哈利波特与魔法石/trimmed_audio/1_HP-01-[AudioTrimmer.com].mp3', sr=None)

# Calculate the maximum absolute amplitude of the audio data
max_amplitude = max(abs(audio_data))

# Define the desired maximum amplitude for normalization
target_amplitude = 0.65

# Calculate the scaling factor for normalization
scaling_factor = target_amplitude / max_amplitude

# Normalize the audio data by scaling it with the scaling factor
normalized_audio = audio_data * scaling_factor

# Save the normalized audio to a new file using soundfile.write()
sf.write('normalized_audio.wav', normalized_audio, 22050)
