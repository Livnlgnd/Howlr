from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
import cv2

from live_stream import LiveStreamController
from discover_page import DiscoverPage


class HowlrApp(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Howlr Live Stream")
        self.setGeometry(100, 100, 360, 640)

        layout = QVBoxLayout()

        self.video_label = QLabel("Camera not started")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.video_label)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        self.start_button = QPushButton("Start Stream")
        self.start_button.clicked.connect(self.start_stream)
        layout.addWidget(self.start_button)

        self.close_button = QPushButton("Close Stream")
        self.close_button.clicked.connect(self.confirm_close)
        self.close_button.setEnabled(False)
        layout.addWidget(self.close_button)

        self.discover_button = QPushButton("Discover Users")
        self.discover_button.clicked.connect(self.open_discover)
        layout.addWidget(self.discover_button)

        self.setLayout(layout)

        self.stream = LiveStreamController(on_frame_callback=self.update_video)

        self.users_online = ["Alice", "Bob", "Charlie", "Diana"]  # Example user list

    def start_stream(self):
        try:
            self.stream.start()
            self.status_label.setText("Streaming live...")
            self.start_button.setEnabled(False)
            self.close_button.setEnabled(True)
        except RuntimeError as e:
            self.status_label.setText(str(e))

    def update_video(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qt_img = QImage(rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_img).scaled(self.video_label.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.video_label.setPixmap(pixmap)

    def confirm_close(self):
        reply = QMessageBox.question(self, "End Stream?", "Are you sure you want to end the stream?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.close_stream()

    def close_stream(self):
        self.stream.stop()
        self.status_label.setText("Stream ended.")
        self.start_button.setEnabled(True)
        self.close_button.setEnabled(False)
        self.video_label.clear()
        self.video_label.setText("Camera not started")

    def closeEvent(self, event):
        self.stream.stop()
        event.accept()

    def open_discover(self):
        self.discover_window = DiscoverPage(self.users_online)
        self.discover_window.show()
