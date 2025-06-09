# gift_manager.py

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import Qt

class Gift:
    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price

# List of gifts with prices
GIFTS = {
    "Rose": Gift("Rose", 10),
    "Chocolate": Gift("Chocolate", 25),
    "Teddy Bear": Gift("Teddy Bear", 50),
    "Book": Gift("Book", 75),
    "Coffee": Gift("Coffee", 100),
    "Hat": Gift("Hat", 200),
    "Sunglasses": Gift("Sunglasses", 350),
    "Watch": Gift("Watch", 500),
    "Perfume": Gift("Perfume", 750),
    "Flowers Bouquet": Gift("Flowers Bouquet", 1000),
    "Smartphone": Gift("Smartphone", 1500),
    "Headphones": Gift("Headphones", 2000),
    "Backpack": Gift("Backpack", 3000),
    "Bicycle": Gift("Bicycle", 4000),
    "Tablet": Gift("Tablet", 5000),
    "Camera": Gift("Camera", 7000),
    "Gaming Console": Gift("Gaming Console", 9000),
    "Laptop": Gift("Laptop", 12000),
    "Drone": Gift("Drone", 15000),
    "Smartwatch": Gift("Smartwatch", 18000),
    "Motorbike": Gift("Motorbike", 22000),
    "Jewelry": Gift("Jewelry", 27000),
    "Designer Bag": Gift("Designer Bag", 32000),
    "Luxury Shoes": Gift("Luxury Shoes", 40000),
    "Car": Gift("Car", 50000),
    "Yacht": Gift("Yacht", 60000),
    "Private Jet": Gift("Private Jet", 70000),
    "Diamond Ring": Gift("Diamond Ring", 80000),
    "Gold Bar": Gift("Gold Bar", 85000),
    "Rare Painting": Gift("Rare Painting", 90000),
    "Luxury Watch": Gift("Luxury Watch", 95000),
    "Supercar": Gift("Supercar", 100000),
    "Rocket": Gift("Rocket", 100000),
    "Castle": Gift("Castle", 95000),
    "Private Island": Gift("Private Island", 90000),
    "Luxury Yacht": Gift("Luxury Yacht", 85000),
    "Exclusive Concert Tickets": Gift("Exclusive Concert Tickets", 80000),
    "VIP Experience": Gift("VIP Experience", 75000),
}

class GiftManager:
    def __init__(self, parent, user_coins):
        self.parent = parent
        self.user_coins = user_coins

    def open_gift_dialog(self, sender, recipient):
        dialog = QDialog(self.parent)
        dialog.setWindowTitle("Send a Gift")
        layout = QVBoxLayout()
        dialog.setLayout(layout)

        # Show sender's coin balance
        balance_label = QLabel(f"Your coins: {self.user_coins.get(sender, 0)}")
        layout.addWidget(balance_label)

        # Create a button for each gift
        for gift_name, gift in GIFTS.items():
            btn = QPushButton(f"{gift.name} - {gift.price} coins")
            layout.addWidget(btn)
            btn.clicked.connect(lambda checked, g=gift: self.try_send_gift(sender, recipient, g, dialog))

        dialog.exec()

    def try_send_gift(self, sender, recipient, gift, dialog):
        coins = self.user_coins.get(sender, 0)
        if coins >= gift.price:
            self.user_coins[sender] -= gift.price
            # Here you would add the gift to recipient's inventory or show animation
            self.parent.show_gift_notification(sender, recipient, gift.name)
            self.parent.show_gift_animation(gift.name)
            dialog.accept()
        else:
            QMessageBox.warning(dialog, "Insufficient Coins", "You don't have enough coins to send this gift.")
