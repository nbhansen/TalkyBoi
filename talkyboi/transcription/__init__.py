"""Transcription components with multi-provider support."""

import logging
from talkyboi.transcription.base import TranscriptionClient
from talkyboi.config import TRANSCRIPTION_PROVIDER

logger = logging.getLogger(__name__)


def create_transcription_client() -> TranscriptionClient:
    """Create a transcription client based on the configured provider.

    The provider is selected via TRANSCRIPTION_PROVIDER environment variable.
    Options: gemini (default), openai, whisper

    Returns:
        TranscriptionClient instance for the configured provider

    Raises:
        ValueError: If the provider is unknown or dependencies are missing
    """
    provider = TRANSCRIPTION_PROVIDER.lower()
    logger.info(f"Creating transcription client for provider: {provider}")

    if provider == "gemini":
        from talkyboi.transcription.gemini_client import GeminiClient
        return GeminiClient()

    elif provider == "openai":
        try:
            from talkyboi.transcription.openai_client import OpenAIClient
            return OpenAIClient()
        except ImportError:
            raise ValueError(
                "OpenAI provider requires the 'openai' package. "
                "Install with: pip install talkyboi[openai]"
            )

    elif provider == "whisper":
        try:
            from talkyboi.transcription.whisper_client import WhisperClient
            return WhisperClient()
        except ImportError:
            raise ValueError(
                "Whisper provider requires the 'faster-whisper' package. "
                "Install with: pip install talkyboi[whisper]"
            )

    else:
        raise ValueError(
            f"Unknown transcription provider: {provider}. "
            "Options: gemini, openai, whisper"
        )
