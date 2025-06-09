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

USERS_FILE = Path("users.json")
CHAT_LOG_FILE = Path("chat_logs.json")

# Helper functions
def load_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def clear_chat():
    with open(CHAT_LOG_FILE, 'w') as f:
        json.dump({"messages": []}, f)

def load_chat():
    if CHAT_LOG_FILE.exists():
        with open(CHAT_LOG_FILE, 'r') as f:
            return json.load(f)
    return {"messages": []}

def save_chat(chat):
    with open(CHAT_LOG_FILE, 'w') as f:
        json.dump(chat, f, indent=4)


# Helper class to stream webcam video to a QLabel
class VideoThread(QObject):
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self, camera_index=0):
        super().__init__()
        self._run_flag = True
        self.cap = cv2.VideoCapture(camera_index)

    def start(self):
        threading.Thread(target=self._capture_loop, daemon=True).start()

    def _capture_loop(self):
        while self._run_flag:
            ret, cv_img = self.cap.read()
            if ret:
                rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                self.change_pixmap_signal.emit(qt_img)
            cv2.waitKey(30)

    def stop(self):
        self._run_flag = False
        self.cap.release()


# Admin panel for user management and clearing chat
class AdminPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Admin Panel")
        self.resize(300, 400)

        self.layout = QVBoxLayout()
        self.user_list = QListWidget()
        self.refresh_button = QPushButton("Refresh Users")
        self.promote_button = QPushButton("Promote to Admin")
        self.delete_button = QPushButton("Delete User")
        self.clear_chat_button = QPushButton("Clear Chat History")

        self.layout.addWidget(QLabel("Registered Users:"))
        self.layout.addWidget(self.user_list)
        self.layout.addWidget(self.refresh_button)
        self.layout.addWidget(self.promote_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.clear_chat_button)

        self.refresh_button.clicked.connect(self.load_users)
        self.promote_button.clicked.connect(self.promote_user)
        self.delete_button.clicked.connect(self.delete_user)
        self.clear_chat_button.clicked.connect(self.clear_chat)

        self.setLayout(self.layout)
        self.load_users()

    def load_users(self):
        self.user_list.clear()
        users = load_users()
        for user, data in users.items():
            role = data.get("role", "user") if isinstance(data, dict) else "user"
            self.user_list.addItem(f"{user} ({role})")

    def promote_user(self):
        selected = self.user_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Error", "Select a user to promote.")
            return
        username = selected.text().split(" ")[0]
        users = load_users()
        if username in users and isinstance(users[username], dict):
            users[username]["role"] = "admin"
            save_users(users)
            QMessageBox.information(self, "Success", f"{username} is now an admin.")
            self.load_users()

    def delete_user(self):
        selected = self.user_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Error", "Select a user to delete.")
            return
        username = selected.text().split(" ")[0]
        if username == "admin":
            QMessageBox.warning(self, "Error", "You can't delete the default admin.")
            return
        users = load_users()
        if username in users:
            del users[username]
            save_users(users)
            QMessageBox.information(self, "Success", f"{username} deleted.")
            self.load_users()

    def clear_chat(self):
        clear_chat()
        QMessageBox.information(self, "Success", "Chat history cleared.")


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


# Window to watch another user's stream (simulated webcam feed or your own for demo)
class StreamWindow(QWidget):
    def __init__(self, current_user, current_streamer_name):
        super().__init__()
        self.current_user = current_user
        self.current_streamer_name = current_streamer_name

        # User coins example; ideally this would come from your user database
        self.user_coins = {
            self.current_user: 150,
            self.current_streamer_name: 0
        }

        self.gift_manager = GiftManager(self, self.user_coins)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Stream Window")
        self.resize(800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Example UI element to show notifications
        self.gift_notification_label = QLabel("")
        self.gift_notification_label.setStyleSheet("color: yellow; font-weight: bold;")
        self.gift_notification_label.setVisible(False)

        # Button to open gifting dialog
        self.gift_button = QPushButton("Send Gift")
        self.gift_button.clicked.connect(self.open_gift_dialog)

        # Add widgets to layout
        self.layout.addWidget(self.gift_button)
        self.layout.addWidget(self.gift_notification_label)

    def open_gift_dialog(self):
        self.gift_manager.open_gift_dialog(self.current_user, self.current_streamer_name)

    def show_gift_animation(self, gift_name):
        anim = GiftAnimationWidget(gift_name, parent=self)
        anim.show()

    def show_gift_notification(self, sender, recipient, gift_name):
        text = f"{sender} sent {gift_name} to {recipient}!"
        self.gift_notification_label.setText(text)
        self.gift_notification_label.setVisible(True)

        # Hide notification after 5 seconds
        QTimer.singleShot(5000, lambda: self.gift_notification_label.setVisible(False))



# Home screen with buttons to go live, discover, profile, logout
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


# Discover window showing all live streams with Join Stream buttons
class DiscoverWindow(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.setWindowTitle("Howlr - Discover")
        self.setGeometry(100, 100, 500, 600)

        layout = QVBoxLayout()

        title = QLabel("Discover Live Streams")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #00ff00;")
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.stream_layout = QVBoxLayout(scroll_content)

        # Add streams for all other users except current
        users = load_users()
        for user in users:
            if user != current_user:
                stream_frame = QFrame()
                stream_frame.setFrameShape(QFrame.Shape.StyledPanel)
                frame_layout = QVBoxLayout()

                user_label = QLabel(f"Live: {user}")
                user_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
                frame_layout.addWidget(user_label)

                # Placeholder for video feed preview (simulate with a label)
                preview_label = QLabel()
                preview_label.setFixedSize(320, 180)
                preview_label.setStyleSheet("background-color: black;")
                frame_layout.addWidget(preview_label)

                join_btn = QPushButton("Join Stream")
                join_btn.clicked.connect(lambda _, u=user: self.join_stream(u))
                frame_layout.addWidget(join_btn)

                stream_frame.setLayout(frame_layout)
                self.stream_layout.addWidget(stream_frame)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        back_btn = QPushButton("Back to Home")
        back_btn.clicked.connect(self.back_to_home)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def join_stream(self, username):
        self.stream_window = StreamWindow(username)
        self.stream_window.show()

    def back_to_home(self):
        self.close()
        self.home = HomeScreen(self.current_user)
        self.home.show()


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
