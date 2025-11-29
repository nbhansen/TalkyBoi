"""Abstract base class for transcription clients."""

from abc import ABC, abstractmethod


class TranscriptionClient(ABC):
    """Base class for all transcription providers."""

    @abstractmethod
    def transcribe(self, audio_bytes: bytes) -> str:
        """Transcribe audio to text.

        Args:
            audio_bytes: WAV audio data as bytes

        Returns:
            Transcribed text
        """
        pass
