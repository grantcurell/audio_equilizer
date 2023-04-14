import os
import argparse
import numpy as np
import librosa
import soundfile as sf
from pydub import AudioSegment
import logging
import concurrent.futures

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define argument parser
parser = argparse.ArgumentParser(description='Apply spectral subtraction and normalization to all audio files in a directory and save the processed files in a new directory.')
parser.add_argument('input_dir', type=str, help='Input directory containing the audio files to be processed.')
parser.add_argument('output_dir', type=str, help='Output directory to save the processed audio files.')
args = parser.parse_args()

# Create the output directory if it doesn't exist
os.makedirs(args.output_dir, exist_ok=True)


def apply_compression(audio_segment, threshold, ratio):
    compressed_audio = audio_segment.empty()
    for chunk in audio_segment[::10]:
        chunk_db = chunk.dBFS
        if chunk_db > threshold:
            difference = chunk_db - threshold
            compressed_chunk = chunk - (difference / ratio)
        else:
            compressed_chunk = chunk
        compressed_audio += compressed_chunk
    return compressed_audio


def process_audio_file(audio_file_path):
    # Load the audio file
    audio_data, sample_rate = librosa.load(audio_file_path, sr=None)

    # Calculate the maximum absolute amplitude of the audio data
    max_amplitude = max(abs(audio_data))

    # Define the desired maximum amplitude for normalization
    target_amplitude = 0.8

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
    output_dir = os.path.join(args.output_dir, os.path.relpath(os.path.dirname(audio_file_path), args.input_dir))
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, os.path.splitext(os.path.basename(audio_file_path))[0] + '_cleaned.mp3')
    sf.write(output_file_path, cleaned_audio, sample_rate)

    # Load the cleaned audio as an AudioSegment
    audio = AudioSegment.from_file(output_file_path, format='wav')

    # Apply dynamic range compression
    amplitude_envelope = audio.dBFS
    threshold = amplitude_envelope + audio.dBFS_std()  # First standard deviation from the mean
    ratio = 4  # Compression ratio, adjust this value as needed
    compressed_audio = apply_compression(audio, threshold, ratio)

    # Save the compressed audio to a new MP3 file
    compressed_output_file_path = os.path.splitext(output_file_path)[0] + '_compressed.mp3'
    compressed_audio.export(compressed_output_file_path, format='mp3')

    logging.info(f"Processed file: {audio_file_path}")


# Loop through all files in the input directory
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    for root, dirs, files in os.walk(args.input_dir):
        for file in files:
            # Check if file is an audio file
            if file.endswith('.mp3') or file.endswith('.wav'):
                audio_file_path = os.path.join(root, file)
                executor.submit(process_audio_file, audio_file_path)
