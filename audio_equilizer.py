import os
import argparse
import numpy as np
import librosa
import soundfile as sf
from pydub import AudioSegment

# Define argument parser
parser = argparse.ArgumentParser(description='Apply spectral subtraction and normalization to all audio files in a directory and save the processed files in a new directory.')
parser.add_argument('input_dir', type=str, help='Input directory containing the audio files to be processed.')
parser.add_argument('output_dir', type=str, help='Output directory to save the processed audio files.')
args = parser.parse_args()

# Create the output directory if it doesn't exist
os.makedirs(args.output_dir, exist_ok=True)

# Loop through all files in the input directory
for root, dirs, files in os.walk(args.input_dir):
    for file in files:
        # Check if file is an audio file
        if file.endswith('.mp3') or file.endswith('.wav'):
            # Load the audio file
            audio_file_path = os.path.join(root, file)
            audio_data, sample_rate = librosa.load(audio_file_path, sr=None)

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
            output_dir = os.path.join(args.output_dir, os.path.relpath(root, args.input_dir))
            os.makedirs(output_dir, exist_ok=True)
            output_file_path = os.path.join(output_dir, os.path.splitext(file)[0] + '_cleaned.mp3')
            sf.write(output_file_path, cleaned_audio, sample_rate)

            # Convert the WAV file to MP3 using pydub
            audio = AudioSegment.from_file(output_file_path, format='mp3')
            audio.export(os.path.splitext(output_file_path)[0] + '.mp3', format='mp3')
