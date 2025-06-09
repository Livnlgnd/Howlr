import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
import threading
import cv2
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit,
    QMessageBox, QListWidget, QTextEdit, QScrollArea, QFrame, QHBoxLayout
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QImage, QPixmap

# Live Stream + Chat Window with webcam feed
class HowlrApp(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Howlr - Live Stream")
        self.setGeometry(100, 100, 480, 640)

        layout = QVBoxLayout()

        # Video display
        self.video_area = QLabel()
        self.video_area.setFixedHeight(320)
        self.video_area.setStyleSheet("background-color: black;")
        layout.addWidget(self.video_area)

        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("background-color: rgba(0, 0, 0, 0.7); color: white; font-size: 14px;")
        layout.addWidget(self.chat_display)

        # Chat input
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Type your message and press Enter...")
        self.chat_input.returnPressed.connect(self.send_message)
        layout.addWidget(self.chat_input)

        # Logout button
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)

        self.setLayout(layout)

        # Start webcam video thread
        self.video_thread = VideoThread(camera_index=0)
        self.video_thread.change_pixmap_signal.connect(self.update_image)
        self.video_thread.start()

        self.load_chat()

    def update_image(self, qt_img):
        self.video_area.setPixmap(QPixmap.fromImage(qt_img).scaled(
            self.video_area.width(), self.video_area.height(), Qt.AspectRatioMode.KeepAspectRatio
        ))

    def send_message(self):
        msg = self.chat_input.text().strip()
        if not msg:
            return
        chat = load_chat()
        chat_entry = f"{self.username}: {msg}"
        chat.setdefault("messages", []).append(chat_entry)
        save_chat(chat)
        self.chat_input.clear()
        self.load_chat()

    def load_chat(self):
        chat = load_chat()
        self.chat_display.clear()
        for line in chat.get("messages", []):
            self.chat_display.append(line)

    def logout(self):
        self.video_thread.stop()
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()

# Profile window showing user info and admin panel access if admin
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


# Login window with user registration and login
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Howlr - Login")
        self.setGeometry(100, 100, 300, 180)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        users = load_users()
        if username in users and users[username] == hashlib.sha256(password.encode()).hexdigest():
            QMessageBox.information(self, "Success", "Login successful!")
            self.close()
            self.home = HomeScreen(username)
            self.home.show()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password.")

    def register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and password.")
            return

        users = load_users()
        if username in users:
            QMessageBox.warning(self, "Error", "Username already exists.")
            return

        users[username] = hashlib.sha256(password.encode()).hexdigest()
        save_users(users)
        QMessageBox.information(self, "Success", "Registration successful! Please login.")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Apply dark mode stylesheet
    dark_stylesheet = """
        QWidget {
            background-color: #121212;
            color: #e0e0e0;
            font-family: Arial, sans-serif;
        }
        QPushButton {
            background-color: #1e7e34;
            color: white;
            border-radius: 5px;
            padding: 8px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #28a745;
        }
        QLineEdit, QTextEdit {
            background-color: #2c2c2c;
            color: white;
            border: 1px solid #444;
            border-radius: 4px;
            padding: 5px;
        }
        QLabel {
            color: #00ff00;
        }
        QScrollArea {
            border: none;
        }
    """
    app.setStyleSheet(dark_stylesheet)

    # Ensure admin user exists
    users = load_users()
    if "admin" not in users:
        users["admin"] = hashlib.sha256("adminpass".encode()).hexdigest()
        save_users(users)

    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec())
