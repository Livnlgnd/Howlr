from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from home_screen import HomeScreen
from admin_panel import AdminPanel
from user_data import load_users  # Assuming this utility is in user_data.py

class ProfileWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Howlr - Profile")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        user_label = QLabel(f"User: {username}")
        user_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        user_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #00ff00;")
        layout.addWidget(user_label)

        users = load_users()
        role = "user"
        if username in users and isinstance(users[username], dict):
            role = users[username].get("role", "user")

        role_label = QLabel(f"Role: {role}")
        role_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        role_label.setStyleSheet("font-size: 14px; color: white;")
        layout.addWidget(role_label)

        if role == "admin":
            admin_btn = QPushButton("Open Admin Panel")
            admin_btn.clicked.connect(self.open_admin_panel)
            layout.addWidget(admin_btn)

        back_btn = QPushButton("Back to Home")
        back_btn.clicked.connect(self.back_to_home)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def open_admin_panel(self):
        self.admin_panel = AdminPanel()
        self.admin_panel.show()

    def back_to_home(self):
        self.close()
        self.home = HomeScreen(self.username)
        self.home.show()
