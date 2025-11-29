"""Transcription worker thread."""

import logging
import numpy as np
from PySide6.QtCore import QThread, Signal
from talkyboi.audio.audio_utils import numpy_to_wav_bytes
from talkyboi.transcription.gemini_client import GeminiClient

logger = logging.getLogger(__name__)


class TranscriptionThread(QThread):
    """Thread that transcribes audio and emits result."""

    finished = Signal(str)
    error = Signal(str)

    def __init__(self, gemini_client: GeminiClient, audio_data: np.ndarray):
        super().__init__()
        self.client = gemini_client
        self.audio_data = audio_data

    def run(self):
        """Run the transcription."""
        try:
            logger.debug("Converting audio to WAV format")
            wav_bytes = numpy_to_wav_bytes(self.audio_data)
            logger.info(f"Transcribing {len(wav_bytes)} bytes of audio")
            result = self.client.transcribe(wav_bytes)
            if result:
                logger.info("Transcription successful")
                self.finished.emit(result)
            else:
                logger.warning("No speech detected in audio")
                self.error.emit("No speech detected")
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            self.error.emit(str(e))
