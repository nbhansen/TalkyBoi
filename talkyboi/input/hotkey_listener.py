"""Global hotkey listener for push-to-talk."""

from pynput import keyboard
from PySide6.QtCore import QObject, Signal
from talkyboi.config import PTT_KEY


class HotkeyListener(QObject):
    """Listens for global keyboard events for push-to-talk.

    Emits ptt_pressed when the PTT key is pressed, and ptt_released when released.
    """

    ptt_pressed = Signal()
    ptt_released = Signal()

    def __init__(self, ptt_key=PTT_KEY):
        super().__init__()
        self.ptt_key = ptt_key
        self._is_pressed = False
        self._listener = None

    def start(self):
        """Start listening for hotkey events."""
        self._listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release,
        )
        self._listener.daemon = True
        self._listener.start()

    def stop(self):
        """Stop the hotkey listener."""
        if self._listener:
            self._listener.stop()
            self._listener = None

    def _on_press(self, key):
        """Handle key press events."""
        if key == self.ptt_key and not self._is_pressed:
            self._is_pressed = True
            self.ptt_pressed.emit()

    def _on_release(self, key):
        """Handle key release events."""
        if key == self.ptt_key and self._is_pressed:
            self._is_pressed = False
            self.ptt_released.emit()
