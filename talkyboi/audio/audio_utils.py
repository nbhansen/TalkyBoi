"""Audio utility functions."""

import io
import numpy as np
from scipy.io import wavfile
from talkyboi.config import SAMPLE_RATE


def numpy_to_wav_bytes(audio_data: np.ndarray) -> bytes:
    """Convert a NumPy array to WAV bytes.

    Args:
        audio_data: NumPy array of audio samples (int16)

    Returns:
        WAV file bytes
    """
    buffer = io.BytesIO()
    wavfile.write(buffer, SAMPLE_RATE, audio_data)
    buffer.seek(0)
    return buffer.read()


def get_audio_duration_ms(audio_data: np.ndarray) -> int:
    """Get the duration of audio data in milliseconds.

    Args:
        audio_data: NumPy array of audio samples

    Returns:
        Duration in milliseconds
    """
    return int(len(audio_data) / SAMPLE_RATE * 1000)
