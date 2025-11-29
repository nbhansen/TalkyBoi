"""OpenAI Whisper API client for transcription."""

import io
import logging
import os
from openai import OpenAI
from talkyboi.transcription.base import TranscriptionClient

logger = logging.getLogger(__name__)


class OpenAIClient(TranscriptionClient):
    """Client for transcribing audio using OpenAI Whisper API."""

    def __init__(self, api_key: str | None = None):
        """Initialize the OpenAI client.

        Args:
            api_key: OpenAI API key. If not provided, reads from OPENAI_API_KEY env var.
        """
        api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found. Set it in .env or pass to constructor."
            )
        self.client = OpenAI(api_key=api_key)
        logger.info("OpenAI Whisper client initialized")

    def transcribe(self, audio_bytes: bytes) -> str:
        """Transcribe audio using OpenAI Whisper API.

        Args:
            audio_bytes: WAV audio data as bytes

        Returns:
            Transcribed text (raw, no cleanup)
        """
        logger.debug(f"Sending {len(audio_bytes)} bytes to OpenAI Whisper API")

        # Wrap bytes in a file-like object with a name
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "audio.wav"

        response = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
        )

        result = response.text.strip()
        logger.debug(f"Received transcription: {len(result)} chars")
        return result
