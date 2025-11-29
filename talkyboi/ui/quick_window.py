"""Quick record window for TalkyBoi."""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QApplication,
)
from PySide6.QtCore import Qt, Signal, QTimer, QElapsedTimer
from PySide6.QtGui import QFont, QScreen


class QuickRecordWindow(QWidget):
    """Minimal window for quick record mode."""

    stop_requested = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("TalkyBoi - Quick Record")
        self.setFixedSize(320, 160)
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground, False)

        # Recording timer
        self._recording_timer = QTimer(self)
        self._recording_timer.timeout.connect(self._update_recording_time)
        self._elapsed_timer = QElapsedTimer()

        # Close timer (for auto-close after success)
        self._close_timer = QTimer(self)
        self._close_timer.setSingleShot(True)
        self._close_timer.timeout.connect(self.close)

        self._setup_ui()
        self._center_on_screen()

    def _setup_ui(self):
        """Set up the user interface."""
        self.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                color: white;
                border-radius: 12px;
            }
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-weight: bold;
                padding: 10px 25px;
                font-size: 13px;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # Status row
        status_layout = QHBoxLayout()
        self.indicator = QLabel("\u25cf")  # Filled circle
        self.indicator.setStyleSheet("color: #e74c3c; font-size: 28px;")
        self.status_label = QLabel("Recording...")
        self.status_label.setFont(QFont("Sans", 12, QFont.Bold))
        self.duration_label = QLabel("0.0s")
        self.duration_label.setStyleSheet("color: #e74c3c; font-size: 14px;")
        self.duration_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        status_layout.addWidget(self.indicator)
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        status_layout.addWidget(self.duration_label)
        layout.addLayout(status_layout)

        # Result preview (hidden initially)
        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)
        self.result_label.setStyleSheet("color: #aaa; font-size: 11px;")
        self.result_label.setMaximumHeight(40)
        self.result_label.hide()
        layout.addWidget(self.result_label)

        # Stop button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.stop_btn = QPushButton("\u25a0  Stop")
        self.stop_btn.clicked.connect(self._on_stop_clicked)
        button_layout.addWidget(self.stop_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Hint text
        self.hint_label = QLabel("Press Esc to stop")
        self.hint_label.setAlignment(Qt.AlignCenter)
        self.hint_label.setStyleSheet("color: #666; font-size: 10px;")
        layout.addWidget(self.hint_label)

    def _center_on_screen(self):
        """Center the window on the primary screen."""
        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
            x = (screen_geometry.width() - self.width()) // 2
            y = (screen_geometry.height() - self.height()) // 2
            self.move(screen_geometry.x() + x, screen_geometry.y() + y)

    def start_recording_ui(self):
        """Start the recording UI state."""
        self._elapsed_timer.start()
        self._recording_timer.start(100)
        self.indicator.setStyleSheet("color: #e74c3c; font-size: 28px;")
        self.status_label.setText("Recording...")
        self.duration_label.setText("0.0s")
        self.duration_label.show()
        self.stop_btn.show()
        self.hint_label.setText("Press Esc to stop")
        self.result_label.hide()

    def _update_recording_time(self):
        """Update the recording duration display."""
        elapsed_ms = self._elapsed_timer.elapsed()
        elapsed_sec = elapsed_ms / 1000.0
        self.duration_label.setText(f"{elapsed_sec:.1f}s")

    def set_transcribing(self):
        """Update UI to show transcribing state."""
        self._recording_timer.stop()
        self.indicator.setStyleSheet("color: #f39c12; font-size: 28px;")
        self.status_label.setText("Transcribing...")
        self.stop_btn.hide()
        self.hint_label.setText("Please wait...")

    def show_success(self, text: str):
        """Show success state with transcribed text preview."""
        self._recording_timer.stop()
        self.indicator.setStyleSheet("color: #27ae60; font-size: 28px;")
        self.indicator.setText("\u2713")  # Checkmark
        self.status_label.setText("Copied to clipboard!")
        self.duration_label.hide()
        self.stop_btn.hide()
        self.hint_label.hide()

        # Show preview of transcribed text
        preview = text[:80] + "..." if len(text) > 80 else text
        self.result_label.setText(f'"{preview}"')
        self.result_label.show()

        # Auto-close after 1.5 seconds
        self._close_timer.start(1500)

    def show_error(self, message: str):
        """Show error state."""
        self._recording_timer.stop()
        self.indicator.setStyleSheet("color: #e74c3c; font-size: 28px;")
        self.indicator.setText("\u2717")  # X mark
        self.status_label.setText("Error")
        self.duration_label.hide()
        self.stop_btn.setText("Close")
        self.stop_btn.clicked.disconnect()
        self.stop_btn.clicked.connect(self.close)
        self.stop_btn.show()
        self.hint_label.setText(message)
        self.result_label.hide()

    def _on_stop_clicked(self):
        """Handle stop button click."""
        self.stop_requested.emit()

    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() in (Qt.Key_Escape, Qt.Key_Return, Qt.Key_Space):
            self.stop_requested.emit()
        else:
            super().keyPressEvent(event)
