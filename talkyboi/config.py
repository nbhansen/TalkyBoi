"""Configuration constants for TalkyBoi."""

import os
from pynput import keyboard

# Audio settings
SAMPLE_RATE = 16000  # 16kHz - good for speech
CHANNELS = 1  # Mono
DTYPE = "int16"  # 16-bit signed

# Push-to-talk key
PTT_KEY = keyboard.Key.ctrl_r  # Right Ctrl

# Gemini settings
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

# Transcription prompt
TRANSCRIPTION_PROMPT = """Transcribe this audio and clean it up for readability.

Instructions:
1. Transcribe the spoken words accurately
2. Remove filler words: "um", "uh", "ah", "er", "like" (filler), "you know", "I mean"
3. Remove false starts and self-corrections (keep corrected version)
4. Remove stutters and repeated words
5. Preserve the speaker's intended meaning exactly
6. Maintain natural sentence structure and punctuation
7. Do NOT paraphrase or change meaning
8. Do NOT add words that weren't spoken

Output only the cleaned transcription, nothing else."""

# UI settings
MIN_RECORDING_DURATION_MS = 500  # Ignore recordings shorter than this
