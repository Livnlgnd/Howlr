import stripe
import webbrowser
from PyQt6.QtWidgets import (
    QDialog, QLabel, QPushButton, QComboBox, QVBoxLayout, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt
import sys

# Your Stripe secret key here (use environment vars for real projects)
STRIPE_SECRET_KEY = "sk_test_51RXw8ABQDR1hq55lMxLZYCHXOsNrPb7Ykitohn1gcCqNnLyPKLGFmz30Z8TY1bRjO3nusl1lrRCnqAIcakJ0HE5o00zWx6ZfsE"

stripe.api_key = STRIPE_SECRET_KEY

COIN_PACKAGES = {
    100: 5.99,
    500: 9.99,
    1000: 19.99,
    2000: 34.99,
    5000: 49.99,
    10000: 59.99,
    20000: 69.99,
    50000: 79.99,
    100000: 99.99,
}

class CoinPurchaseDialog(QDialog):
    def __init__(self, username, user_coins: dict, parent=None):
        super().__init__(parent)
        self.username = username
        self.user_coins = user_coins
        self.setWindowTitle("Buy Coins")
        self.setFixedSize(300, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.balance_label = QLabel()
        self.balance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.balance_label)

        self.info_label = QLabel("Select a coin package to purchase:")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label)

        self.coin_selector = QComboBox()
        for coins, price in COIN_PACKAGES.items():
            self.coin_selector.addItem(f"{coins} coins - ${price:.2f}", (coins, price))
        self.coin_selector.currentIndexChanged.connect(self.update_price_label)
        layout.addWidget(self.coin_selector)

        self.price_label = QLabel()
        self.price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.price_label)

        buy_button = QPushButton("Buy")
        buy_button.clicked.connect(self.buy_coins)
        layout.addWidget(buy_button)

        self.setLayout(layout)
        self.update_balance_label()
        self.update_price_label(0)

    def update_balance_label(self):
        balance = self.user_coins.get(self.username, 0)
        self.balance_label.setText(f"Your current coin balance: {balance}")

    def update_price_label(self, index):
        coins, price = self.coin_selector.currentData()
        self.price_label.setText(f"Price: ${price:.2f} for {coins} coins")

    def buy_coins(self):
        coins, price = self.coin_selector.currentData()
        try:
            # Create Stripe Checkout Session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'{coins} Coins Package',
                        },
                        'unit_amount': int(price * 100),  # price in cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://your-domain.com/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='https://your-domain.com/cancel',
                metadata={
                    "username": self.username,
                    "coins": str(coins)
                }
            )

            # Open the checkout page in default browser
            webbrowser.open(session.url)

            # NOTE:
            # You should implement a backend webhook listener to confirm payment,
            # then update the user's coins balance securely.
            # Here we just notify user to complete payment in browser.
            QMessageBox.information(self, "Redirecting to Payment",
                                    "You will be redirected to Stripe to complete your purchase.\n"
                                    "After payment, coins will be added to your balance.")

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Payment Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    user_coins = {"alice": 120}  # Example balances
    dlg = CoinPurchaseDialog("alice", user_coins)
    dlg.exec()

    print("User balances:", user_coins)
