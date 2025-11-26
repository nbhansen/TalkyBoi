"""Main window for TalkyBoi."""

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QLabel,
    QApplication,
)
from PySide6.QtCore import Qt, Slot, Signal, QEvent
from PySide6.QtGui import QFont


class HoldButton(QPushButton):
    """A button that emits signals on press and release."""

    pressed_signal = Signal()
    released_signal = Signal()

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(
            "QPushButton { background-color: #4a90d9; color: white; "
            "font-weight: bold; padding: 15px 30px; font-size: 14px; }"
            "QPushButton:pressed { background-color: #e74c3c; }"
        )

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.pressed_signal.emit()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.released_signal.emit()


class MainWindow(QMainWindow):
    """Main application window."""

    # Signals for keyboard PTT
    ptt_pressed = Signal()
    ptt_released = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("TalkyBoi")
        self.setMinimumSize(500, 400)
        self._ptt_key_held = False

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Status bar at top
        status_layout = QHBoxLayout()
        self.recording_indicator = QLabel("\u25cf")  # Filled circle
        self.recording_indicator.setStyleSheet("color: gray; font-size: 24px;")
        self.status_label = QLabel("Ready - Hold F5 or click button")
        status_layout.addWidget(self.recording_indicator)
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        layout.addLayout(status_layout)

        # Text area for transcription
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setPlaceholderText("Transcribed text will appear here...")
        self.text_area.setFont(QFont("Sans", 11))
        layout.addWidget(self.text_area)

        # Hold to talk button (centered)
        talk_layout = QHBoxLayout()
        talk_layout.addStretch()
        self.talk_btn = HoldButton("Hold to Talk")
        talk_layout.addWidget(self.talk_btn)
        talk_layout.addStretch()
        layout.addLayout(talk_layout)

        # Button bar at bottom
        button_layout = QHBoxLayout()
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_text)
        self.copy_btn = QPushButton("Copy All")
        self.copy_btn.clicked.connect(self.copy_all)
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.copy_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Install event filter to catch all key events
        QApplication.instance().installEventFilter(self)

    def eventFilter(self, obj, event):
        """Catch key events application-wide when window is active."""
        if self.isActiveWindow():
            if event.type() == QEvent.KeyPress and not event.isAutoRepeat():
                if event.key() == Qt.Key_F5:
                    if not self._ptt_key_held:
                        self._ptt_key_held = True
                        self.ptt_pressed.emit()
                    return True
            elif event.type() == QEvent.KeyRelease and not event.isAutoRepeat():
                if event.key() == Qt.Key_F5:
                    if self._ptt_key_held:
                        self._ptt_key_held = False
                        self.ptt_released.emit()
                    return True
        return super().eventFilter(obj, event)

    @Slot()
    def clear_text(self):
        """Clear the text area."""
        self.text_area.clear()

    @Slot()
    def copy_all(self):
        """Copy all text to clipboard."""
        text = self.text_area.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self.status_label.setText("Copied to clipboard!")

    def set_recording(self, is_recording: bool):
        """Update UI to show recording state."""
        if is_recording:
            self.recording_indicator.setStyleSheet("color: red; font-size: 24px;")
            self.status_label.setText("Recording...")
        else:
            self.recording_indicator.setStyleSheet("color: gray; font-size: 24px;")
            self.status_label.setText("Ready")

    def set_transcribing(self):
        """Update UI to show transcribing state."""
        self.status_label.setText("Transcribing...")

    def append_transcription(self, text: str):
        """Append transcribed text to the text area."""
        current = self.text_area.toPlainText()
        if current:
            self.text_area.setPlainText(current + "\n\n" + text)
        else:
            self.text_area.setPlainText(text)
        # Scroll to bottom
        scrollbar = self.text_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        self.status_label.setText("Ready")

    def show_error(self, message: str):
        """Show an error message in the status bar."""
        self.status_label.setText(f"Error: {message}")
        self.recording_indicator.setStyleSheet("color: gray; font-size: 24px;")
