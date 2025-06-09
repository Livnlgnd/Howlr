# main.py

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from profile_page import ProfilePage
from howlr_ui import HowlrApp
from user_profile import UserProfile
from discover_page import DiscoverPage


class MainWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Howlr - Main Window")
        self.setGeometry(100, 100, 400, 700)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Main live stream widget
        self.stream_widget = HowlrApp(self.username)
        self.layout.addWidget(self.stream_widget)

        # Buttons panel
        self.profile_btn = QPushButton("Open Profile")
        self.profile_btn.clicked.connect(self.open_profile)
        self.layout.addWidget(self.profile_btn)


        # Style buttons and background (matte black and white)
        self.setStyleSheet("""
            QWidget {
                background-color: #0a0a0a;
                color: white;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }
            QPushButton {
                background-color: #f2f2f2;
                color: #000;
                border-radius: 10px;
                padding: 10px;
                margin: 5px 0;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

        # Keep references to opened windows
        self.profile_window = None
        self.discover_window = None

    def open_profile(self):
        if self.profile_window is None:
            self.profile_window = ProfilePage(self.username)
            self.profile_window.show()
            self.profile_window.destroyed.connect(self.on_profile_closed)

    def on_profile_closed(self):
        self.profile_window = None

    def open_discover(self):
        if self.discover_window is None:
            # Example users_online list; replace with your live data
            users_online = ["alice", "bob", "charlie"]
            self.discover_window = DiscoverPage(users_online)
            self.discover_window.show()
            self.discover_window.destroyed.connect(self.on_discover_closed)

    def on_discover_closed(self):
        self.discover_window = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    username = "TestUser"  # or fetch actual logged-in username
    main_window = MainWindow(username)
    main_window.show()
    sys.exit(app.exec())
