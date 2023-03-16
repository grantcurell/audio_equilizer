from pydub import AudioSegment

# Set target dBFS level
target_dBFS = -24

# Load audio file
audio = AudioSegment.from_file('../1哈利波特与魔法石/trimmed_audio/1_HP-01-[AudioTrimmer.com].mp3', format="mp3")

# Normalize audio to target dBFS level
normalized_audio = audio.normalize(target_dBFS)

# Write normalized audio to new file
normalized_audio.export("normalized_audiofile.mp3", format="mp3")
