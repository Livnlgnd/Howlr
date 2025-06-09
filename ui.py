# howlr_ui.py
import cv2
import threading
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap, QFont
from live_stream import LiveStreamController
from howlr_ui import HowlrApp  # ✅ Correct



class HowlrApp(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"Howlr - Live as {username}")
        self.setGeometry(100, 100, 400, 700)

        self.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #111111, stop:1 #1f1f1f
                );
                color: white;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }

            QPushButton {
                background-color: #34d399;  /* emerald-400 */
                color: black;
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #10b981; /* emerald-500 */
            }

            QLabel#usernameLabel {
                font-size: 18px;
                font-weight: bold;
                color: #34d399;
            }

            QLabel#statusLabel {
                color: #cccccc;
                font-size: 14px;
            }

            QLabel#viewersLabel {
                font-size: 13px;
                color: #999999;
            }
        """)

        self.init_ui()
        self.stream = LiveStreamController(on_frame_callback=self.update_video)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(16, 16, 16, 16)

        self.username_label = QLabel(f"@{self.username}")
        self.username_label.setObjectName("usernameLabel")
        self.username_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.username_label)

        self.video_label = QLabel("Camera not started")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setFixedHeight(480)
        self.video_label.setStyleSheet("background-color: #000; border-radius: 12px;")
        layout.addWidget(self.video_label)

        self.status_label = QLabel("Not live")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        self.viewers_label = QLabel("👥 Viewers: 0")
        self.viewers_label.setObjectName("viewersLabel")
        self.viewers_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.viewers_label)

        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Stream")
        self.start_button.clicked.connect(self.start_stream)
        button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("End Stream")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.confirm_close)
        button_layout.addWidget(self.stop_button)

        layout.addLayout(button_layout)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.setLayout(layout)

        # Simulated viewer count
        self.viewer_timer = QTimer()
        self.viewer_timer.timeout.connect(self.update_viewers)

    def start_stream(self):
        try:
            self.stream.start()
            self.status_label.setText("🔴 LIVE")
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.viewer_timer.start(3000)  # Update viewers every 3s
        except RuntimeError as e:
            self.status_label.setText(str(e))

    def update_video(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qt_img = QImage(rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_img).scaled(
            self.video_label.width(), self.video_label.height(),
            Qt.AspectRatioMode.KeepAspectRatio
        )
        self.video_label.setPixmap(pixmap)

    def update_viewers(self):
        import random
        viewers = random.randint(1, 200)
        self.viewers_label.setText(f"👥 Viewers: {viewers}")

    def confirm_close(self):
        reply = QMessageBox.question(self, "End Stream?", "Are you sure you want to end the stream?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.close_stream()

    def close_stream(self):
        self.stream.stop()
        self.viewer_timer.stop()
        self.status_label.setText("Stream ended.")
        self.viewers_label.setText("👥 Viewers: 0")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.video_label.clear()
        self.video_label.setText("Camera not started")

    def closeEvent(self, event):
        self.stream.stop()
        self.viewer_timer.stop()
        event.accept()
