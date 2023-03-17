# Audio Fixer

- [Audio Fixer](#audio-fixer)
  - [The Problem](#the-problem)
  - [Visualization](#visualization)
    - [Original File](#original-file)
    - [Original File Sample](#original-file-sample)
    - [Cleaned File](#cleaned-file)
    - [Cleaned File Sample](#cleaned-file-sample)
    - [But They are the Same](#but-they-are-the-same)
  - [Definitions](#definitions)
    - [What is dBFS?](#what-is-dbfs)
    - [Maximum Absolute Amplitude](#maximum-absolute-amplitude)


## The Problem

My wonderful Chinese teacher sent me a full radio reading of Harry Potter (哈利波特) but it sounded... well... terrible. I could barely listen to it.

## Visualization

### Original File

![](images/2023-03-16-19-24-57.png)

Generated with [this code](visualize_audio.py)

This is an analysis of the original audio file. The most indicative graph is #3 where 0 is the loudest possible sound the audio format will accept. As you can see, a high percentage of the original audio file was getting close to 0 so it sounded *very* loud.

### Original File Sample

[This is the first chapter unfiltered](audio_files/1_HP-01-[AudioTrimmer.com].mp3)

### Cleaned File

![](images/2023-03-16-19-33-51.png)

Generated with [this code](visualize_audio.py)

### Cleaned File Sample

[This is the first chapter cleaned](audio_files/1_HP-01-[AudioTrimmer.com]_cleaned.mp3)

### But They are the Same

Yes, because we maintained the audio characteristics of the file largely the same, the dynamic range and the relative amplitude are the same. However, if you compare the noise and the absolute amplitude you can see that they have changed.

![](images/2023-03-16-20-11-03.png)

Generated with [this code](compare_absolute_amplitude.py)

In the lower chart you can see how the green line rockets upward. That is the background hum you hear in the original audio file.

## Definitions

### What is dBFS?

dBFS stands for decibels relative to full scale, and it is a unit of measurement used to express the level or amplitude of a digital audio signal.

In a digital audio system, the full scale represents the maximum possible amplitude that can be represented by the system. The dBFS scale is a logarithmic scale that expresses the ratio of the signal level to the full scale level, in decibels. A signal level that is equal to the full scale level corresponds to 0 dBFS, while a level that is half of the full scale level corresponds to -6 dBFS, and a level that is one-tenth of the full scale level corresponds to -20 dBFS, and so on.

The use of dBFS is important because digital audio signals can be easily clipped or distorted if they exceed the full scale level. By monitoring and controlling the dBFS level of digital audio signals, we can ensure that they remain within the safe operating range of the system and avoid clipping or distortion.

### Maximum Absolute Amplitude

The maximum absolute amplitude of an audio signal is the largest magnitude of the audio samples within the signal. It represents the maximum displacement of the audio waveform from its zero or neutral position.

In digital audio, the maximum absolute amplitude is typically represented by a signed integer or floating point number that corresponds to the maximum possible value that can be represented by the audio system. For example, in a 16-bit audio system, the maximum absolute amplitude is represented by the value 32767 (assuming a signed representation), while in a 24-bit audio system, the maximum absolute amplitude is represented by the value 8388607.

Knowing the maximum absolute amplitude of an audio signal is important for a number of reasons, including setting appropriate levels for recording and playback, preventing clipping and distortion, and applying normalization or other signal processing techniques to ensure that the signal remains within the safe operating range of the system.