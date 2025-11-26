"""Transcription worker thread."""

import numpy as np
from PySide6.QtCore import QThread, Signal
from talkyboi.audio.audio_utils import numpy_to_wav_bytes
from talkyboi.transcription.gemini_client import GeminiClient


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
            wav_bytes = numpy_to_wav_bytes(self.audio_data)
            result = self.client.transcribe(wav_bytes)
            if result:
                self.finished.emit(result)
            else:
                self.error.emit("No speech detected")
        except Exception as e:
            self.error.emit(str(e))
