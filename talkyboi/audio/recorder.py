"""Audio recording with sounddevice."""

import numpy as np
import sounddevice as sd
from PySide6.QtCore import QObject, Signal, QThread
from talkyboi.config import SAMPLE_RATE, CHANNELS, DTYPE


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
            return

        self._is_recording = True
        self._audio_buffer = []

        try:
            self._stream = sd.InputStream(
                samplerate=SAMPLE_RATE,
                channels=CHANNELS,
                dtype=DTYPE,
                callback=self._audio_callback,
            )
            self._stream.start()
        except Exception as e:
            self._is_recording = False
            self.error_occurred.emit(f"Failed to start recording: {e}")

    def stop_recording(self):
        """Stop recording and emit the recorded audio."""
        if not self._is_recording:
            return

        self._is_recording = False

        try:
            self._stream.stop()
            self._stream.close()
        except Exception:
            pass

        if self._audio_buffer:
            audio_data = np.concatenate(self._audio_buffer)
            self.recording_finished.emit(audio_data)
        else:
            self.error_occurred.emit("No audio recorded")

    def _audio_callback(self, indata, frames, time, status):
        """Callback for sounddevice stream - accumulates audio samples."""
        if status:
            print(f"Audio status: {status}")
        if self._is_recording:
            self._audio_buffer.append(indata.copy().flatten())

    @property
    def is_recording(self) -> bool:
        """Return whether currently recording."""
        return self._is_recording
