"""Gemini API client for transcription."""

import os
from google import genai
from google.genai import types
from talkyboi.config import GEMINI_MODEL, TRANSCRIPTION_PROMPT


class GeminiClient:
    """Client for transcribing audio using Gemini API."""

    def __init__(self, api_key: str | None = None):
        """Initialize the Gemini client.

        Args:
            api_key: Gemini API key. If not provided, reads from GEMINI_API_KEY env var.
        """
        api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. Set it in .env or pass to constructor."
            )
        self.client = genai.Client(api_key=api_key)
        self.model = GEMINI_MODEL

    def transcribe(self, audio_bytes: bytes) -> str:
        """Transcribe audio and clean it up.

        Args:
            audio_bytes: WAV audio data as bytes

        Returns:
            Cleaned transcription text
        """
        response = self.client.models.generate_content(
            model=self.model,
            contents=[
                TRANSCRIPTION_PROMPT,
                types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav"),
            ],
        )
        return response.text.strip()
