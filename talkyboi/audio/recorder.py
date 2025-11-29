"""Audio recording with sounddevice."""

import logging
import numpy as np
import sounddevice as sd
from PySide6.QtCore import QObject, Signal, QThread
from talkyboi.config import SAMPLE_RATE, CHANNELS, DTYPE

logger = logging.getLogger(__name__)


class AudioRecorder(QObject):
    """Records audio from the microphone.

    Emits recording_finished signal with audio data when recording stops.
    """

    recording_finished = Signal(np.ndarray)
    error_occurred = Signal(str)

    def __init__(self):
        super().__init__()
        self._is_recording = False
        self._audio_buffer = []

    def start_recording(self):
        """Start recording audio from the default microphone."""
        if self._is_recording:
            logger.warning("Already recording, ignoring start request")
            return

        self._is_recording = True
        self._audio_buffer = []

        try:
            logger.debug(f"Opening audio stream: {SAMPLE_RATE}Hz, {CHANNELS}ch, {DTYPE}")
            self._stream = sd.InputStream(
                samplerate=SAMPLE_RATE,
                channels=CHANNELS,
                dtype=DTYPE,
                callback=self._audio_callback,
            )
            self._stream.start()
            logger.info("Recording started")
        except Exception as e:
            logger.error(f"Failed to start recording: {e}")
            self._is_recording = False
            self.error_occurred.emit(f"Failed to start recording: {e}")

    def stop_recording(self):
        """Stop recording and emit the recorded audio."""
        if not self._is_recording:
            logger.warning("Not recording, ignoring stop request")
            return

        self._is_recording = False

        try:
            self._stream.stop()
            self._stream.close()
            logger.debug("Audio stream closed")
        except Exception as e:
            logger.warning(f"Error closing stream: {e}")

        if self._audio_buffer:
            audio_data = np.concatenate(self._audio_buffer)
            logger.info(f"Recording stopped: {len(audio_data)} samples captured")
            self.recording_finished.emit(audio_data)
        else:
            logger.warning("No audio data captured")
            self.error_occurred.emit("No audio recorded")

    def _audio_callback(self, indata, frames, time, status):
        """Callback for sounddevice stream - accumulates audio samples."""
        if status:
            logger.warning(f"Audio stream status: {status}")
        if self._is_recording:
            self._audio_buffer.append(indata.copy().flatten())

    @property
    def is_recording(self) -> bool:
        """Return whether currently recording."""
        return self._is_recording
