"""Local Whisper client for transcription using faster-whisper."""

import io
import logging
import os
from faster_whisper import WhisperModel
from talkyboi.transcription.base import TranscriptionClient

logger = logging.getLogger(__name__)

# Default model - "base" is a good balance of speed and accuracy
# Options: tiny, base, small, medium, large-v2, large-v3
WHISPER_MODEL = os.environ.get("WHISPER_MODEL", "base")


class WhisperClient(TranscriptionClient):
    """Client for transcribing audio using local Whisper model."""

    def __init__(self, model_size: str | None = None):
        """Initialize the local Whisper client.

        Args:
            model_size: Whisper model size. If not provided, reads from WHISPER_MODEL env var.
                       Options: tiny, base, small, medium, large-v2, large-v3
        """
        model_size = model_size or WHISPER_MODEL
        logger.info(f"Loading Whisper model: {model_size} (this may take a moment on first run)")

        # Use CPU by default, auto-detect CUDA if available
        # int8 quantization for faster inference on CPU
        self.model = WhisperModel(model_size, device="auto", compute_type="auto")
        logger.info(f"Whisper model '{model_size}' loaded successfully")

    def transcribe(self, audio_bytes: bytes) -> str:
        """Transcribe audio using local Whisper model.

        Args:
            audio_bytes: WAV audio data as bytes

        Returns:
            Transcribed text (raw, no cleanup)
        """
        logger.debug(f"Transcribing {len(audio_bytes)} bytes with local Whisper")

        # faster-whisper can read from file-like objects
        audio_file = io.BytesIO(audio_bytes)

        segments, info = self.model.transcribe(audio_file, language="en")

        # Concatenate all segments
        text = " ".join(segment.text.strip() for segment in segments)

        logger.debug(f"Received transcription: {len(text)} chars (detected language: {info.language})")
        return text
