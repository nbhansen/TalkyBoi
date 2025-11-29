#!/usr/bin/env python3
"""TalkyBoi - Audio dictation with Gemini transcription."""

import logging
import sys
from dotenv import load_dotenv

# Configure logging before importing app modules
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler(sys.stderr)],
)

load_dotenv()

from talkyboi.app import run

if __name__ == "__main__":
    run()
