from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from user_profile import ProfileWindow
from howlr_ui import HowlrApp


class HomeScreen(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Howlr - Home")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        welcome_label = QLabel(f"Welcome, {username}!")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #00ff00;")
        layout.addWidget(welcome_label)

        profile_btn = QPushButton("Profile")
        profile_btn.setStyleSheet("background-color: #f0f0f0; color: black;")  # matte white button style
        profile_btn.clicked.connect(self.open_profile)
        layout.addWidget(profile_btn)

        live_stream_btn = QPushButton("Go Live")
        live_stream_btn.setStyleSheet("background-color: #f0f0f0; color: black;")
        live_stream_btn.clicked.connect(self.open_live_stream)
        layout.addWidget(live_stream_btn)

        self.setLayout(layout)

    def open_profile(self):
        self.profile_window = ProfileWindow(self.username)
        self.profile_window.show()

    def open_live_stream(self):
        self.live_stream_window = HowlrApp(self.username)
        self.live_stream_window.show()
        self.close()
