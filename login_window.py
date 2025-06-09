import hashlib
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from home_screen import HomeScreen
from user_data import load_users, save_users  # Assuming user persistence in user_data.py

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
