#!/usr/bin/env python3
"""TalkyBoi - Audio dictation with Gemini transcription."""

import argparse
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

from talkyboi.app import run, run_quick

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="TalkyBoi - Audio dictation with Gemini transcription"
    )
    parser.add_argument(
        "--quick", "-q",
        action="store_true",
        help="Quick record mode: record, transcribe, copy to clipboard, exit"
    )
    args = parser.parse_args()

    if args.quick:
        run_quick()
    else:
        run()
