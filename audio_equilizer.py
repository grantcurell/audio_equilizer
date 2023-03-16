import numpy as np
import librosa
import soundfile as sf
from pydub import AudioSegment

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

# Apply spectral subtraction to the audio data
stft = librosa.stft(normalized_audio)
magnitude = np.abs(stft)
phase = np.exp(1.0j * np.angle(stft))
noise_magnitude = np.mean(magnitude[:, :800], axis=1)
cleaned_magnitude = np.maximum(magnitude - noise_magnitude[:, np.newaxis], 0.0)
cleaned_stft = cleaned_magnitude * phase
cleaned_audio = librosa.istft(cleaned_stft)

# Save the cleaned audio to a new WAV file using soundfile.write()
sf.write('cleaned_audio.wav', cleaned_audio, sample_rate)

# Convert the WAV file to MP3 using pydub
audio = AudioSegment.from_wav('cleaned_audio.wav')
audio.export('cleaned_audio.mp3', format='mp3')
