from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QDialog, QComboBox, QMessageBox
from PyQt6.QtCore import QTimer
import requests
import webbrowser

class ProfilePage(QWidget):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.username = username
        self.init_ui()
        self.load_coin_balance()

    def init_ui(self):
        self.setWindowTitle(f"{self.username}'s Profile")
        layout = QVBoxLayout(self)

        self.coin_label = QLabel("Coins: Loading...", self)
        layout.addWidget(self.coin_label)

        refresh_btn = QPushButton("🔄 Refresh Coins", self)
        refresh_btn.clicked.connect(self.load_coin_balance)
        layout.addWidget(refresh_btn)

        buy_btn = QPushButton("💰 Buy Coins", self)
        buy_btn.clicked.connect(self.open_coin_dialog)
        layout.addWidget(buy_btn)

    def load_coin_balance(self):
        try:
            response = requests.get(f"http://localhost:5000/user-coins/{self.username}")
            data = response.json()
            coins = data.get("coins", 0)
            self.coin_label.setText(f"Coins: {coins}")
        except Exception as e:
            self.coin_label.setText("Coins: Error")
            print("Failed to load coins:", e)

    def open_coin_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Buy Coins")
        dialog.resize(300, 100)

        combo = QComboBox(dialog)
        combo.addItems(["100_coins", "1000_coins", "10000_coins"])
        combo.setGeometry(20, 20, 200, 30)

        buy_btn = QPushButton("Buy", dialog)
        buy_btn.setGeometry(220, 20, 60, 30)

        def buy_selected():
            package = combo.currentText()
            dialog.accept()
            self.start_checkout(package)

        buy_btn.clicked.connect(buy_selected)
        dialog.exec()

    def start_checkout(self, package):
        try:
            payload = {"username": self.username, "package": package}
            response = requests.post("http://localhost:5000/create-checkout-session", json=payload)
            checkout_url = response.json().get("checkout_url")

            if checkout_url:
                webbrowser.open(checkout_url)
            else:
                raise Exception("No checkout URL returned")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to initiate payment: {e}")
