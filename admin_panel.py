from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel, QMessageBox)
from storage import load_users, save_users, clear_chat

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
