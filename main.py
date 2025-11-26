#!/usr/bin/env python3
"""TalkyBoi - Audio dictation with Gemini transcription."""

from dotenv import load_dotenv

load_dotenv()

from talkyboi.app import run

if __name__ == "__main__":
    run()
