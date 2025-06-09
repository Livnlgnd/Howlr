from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from howlr_app import HowlrApp
from discover_window import DiscoverWindow
from profile_window import ProfileWindow
from login_window import LoginWindow

class HomeScreen(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Howlr - Home")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        welcome_label = QLabel(f"Welcome, {username}!")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #00ff00;")
        layout.addWidget(welcome_label)

        go_live_btn = QPushButton("Go Live")
        go_live_btn.clicked.connect(self.go_live)
        layout.addWidget(go_live_btn)

        discover_btn = QPushButton("Discover")
        discover_btn.clicked.connect(self.open_discover)
        layout.addWidget(discover_btn)

        profile_btn = QPushButton("Profile")
        profile_btn.clicked.connect(self.open_profile)
        layout.addWidget(profile_btn)

        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)

        self.setLayout(layout)

    def go_live(self):
        self.close()
        self.live_window = HowlrApp(self.username)
        self.live_window.show()

    def open_discover(self):
        self.close()
        self.discover_window = DiscoverWindow(self.username)
        self.discover_window.show()

    def open_profile(self):
        self.close()
        self.profile_window = ProfileWindow(self.username)
        self.profile_window.show()

    def logout(self):
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()
