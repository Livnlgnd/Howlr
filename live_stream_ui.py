from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit, QFrame
)
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtCore import Qt

class MobileStyleLiveStreamUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Howlr Live Stream")
        self.resize(360, 640)  # typical mobile screen ratio

        # Set matte gradient background
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #222222, stop:1 #121212
                );
                color: white;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # Video placeholder (simulate video with a dark frame)
        self.video_frame = QFrame()
        self.video_frame.setFixedHeight(300)
        self.video_frame.setStyleSheet("""
            QFrame {
                background-color: #000000;
                border-radius: 16px;
            }
        """)
        main_layout.addWidget(self.video_frame)

        # Chat overlay area (transparent black with emoji-only text)
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background: rgba(0, 0, 0, 0.4);
                border-radius: 12px;
                padding: 8px;
                font-size: 18px;
                color: white;
                font-weight: 600;
                font-family: 'Segoe UI Emoji', 'Segoe UI Symbol', sans-serif;
            }
        """)
        self.chat_display.setFixedHeight(150)
        main_layout.addWidget(self.chat_display)

        # Input area with rounded line edit and send button
        input_layout = QHBoxLayout()
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Type emojis here...")
        self.chat_input.setStyleSheet("""
            QLineEdit {
                background-color: #f5f5f5;
                border-radius: 20px;
                padding: 8px 16px;
                font-size: 16px;
            }
        """)
        input_layout.addWidget(self.chat_input)

        self.send_button = QPushButton("Send")
        self.send_button.setFixedWidth(80)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                border-radius: 20px;
                font-weight: bold;
                color: #121212;
            }
            QPushButton:hover {
                background-color: #c0c0c0;
            }
        """)
        input_layout.addWidget(self.send_button)

        main_layout.addLayout(input_layout)

        # Control buttons area
        controls_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Stream")
        self.start_button.setStyleSheet(self._matte_button_style())
        controls_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Stream")
        self.stop_button.setStyleSheet(self._matte_button_style())
        controls_layout.addWidget(self.stop_button)

        main_layout.addLayout(controls_layout)

        self.setLayout(main_layout)

        # Connect send button
        self.send_button.clicked.connect(self._send_chat_message)

    def _send_chat_message(self):
        text = self.chat_input.text()
        if text.strip():
            # Append message to chat display
            self.chat_display.append(text)
            self.chat_input.clear()

    def _matte_button_style(self):
        return """
            QPushButton {
                background-color: #ffffff;
                color: #222222;
                border-radius: 20px;
                padding: 10px 20px;
                font-weight: 600;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #bdbdbd;
            }
        """

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MobileStyleLiveStreamUI()
    window.show()
    sys.exit(app.exec())
