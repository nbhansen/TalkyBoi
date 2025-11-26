"""Application setup for TalkyBoi."""

import sys
import os
from PySide6.QtWidgets import QApplication, QMessageBox
from talkyboi.ui.main_window import MainWindow
from talkyboi.audio.recorder import AudioRecorder
from talkyboi.audio.audio_utils import get_audio_duration_ms
from talkyboi.transcription.gemini_client import GeminiClient
from talkyboi.transcription.transcriber import TranscriptionThread
from talkyboi.config import MIN_RECORDING_DURATION_MS


class TalkyBoiApp:
    """Main application controller that wires all components together."""

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("TalkyBoi")

        # Check for API key
        if not os.environ.get("GEMINI_API_KEY"):
            QMessageBox.critical(
                None,
                "Missing API Key",
                "GEMINI_API_KEY not found.\n\nCreate a .env file with:\nGEMINI_API_KEY=your_key_here",
            )
            sys.exit(1)

        # Initialize components
        self.window = MainWindow()
        self.recorder = AudioRecorder()
        self.gemini_client = GeminiClient()
        self.transcription_thread = None

        # Connect signals
        self._connect_signals()

    def _connect_signals(self):
        """Connect all component signals."""
        # Keyboard PTT (Ctrl key when app focused)
        self.window.ptt_pressed.connect(self._on_ptt_pressed)
        self.window.ptt_released.connect(self._on_ptt_released)

        # Talk button -> Recording
        self.window.talk_btn.pressed_signal.connect(self._on_ptt_pressed)
        self.window.talk_btn.released_signal.connect(self._on_ptt_released)

        # Recording -> Transcription
        self.recorder.recording_finished.connect(self._on_recording_finished)
        self.recorder.error_occurred.connect(self.window.show_error)

    def _on_ptt_pressed(self):
        """Handle push-to-talk key pressed."""
        self.recorder.start_recording()
        self.window.set_recording(True)

    def _on_ptt_released(self):
        """Handle push-to-talk key released."""
        self.recorder.stop_recording()
        self.window.set_recording(False)

    def _on_recording_finished(self, audio_data):
        """Handle recording finished - start transcription."""
        duration = get_audio_duration_ms(audio_data)

        if duration < MIN_RECORDING_DURATION_MS:
            self.window.show_error(f"Recording too short ({duration}ms)")
            return

        self.window.set_transcribing()

        # Create new thread for this transcription
        self.transcription_thread = TranscriptionThread(self.gemini_client, audio_data)
        self.transcription_thread.finished.connect(self._on_transcription_done)
        self.transcription_thread.error.connect(self._on_transcription_error)
        self.transcription_thread.start()

    def _on_transcription_done(self, text):
        """Handle transcription completed."""
        self.window.append_transcription(text)

    def _on_transcription_error(self, error):
        """Handle transcription error."""
        self.window.show_error(error)

    def run(self):
        """Run the application."""
        self.window.show()
        result = self.app.exec()
        if self.transcription_thread and self.transcription_thread.isRunning():
            self.transcription_thread.quit()
            self.transcription_thread.wait()
        return result


def run():
    """Run the TalkyBoi application."""
    app = TalkyBoiApp()
    sys.exit(app.run())
