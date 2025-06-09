from PyQt6.QtWidgets import (
    QDialog, QLabel, QPushButton, QComboBox, QVBoxLayout,
    QMessageBox, QWidget
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QDateTime
from PyQt6.QtGui import QFont


class GiftDialog(QDialog):
    GIFTS = {
        "Rose": {"cost": 10, "image": "assets/gifts/rose.png"},
        "Teddy Bear": {"cost": 50, "image": "assets/gifts/teddy.png"},
        "Diamond": {"cost": 100, "image": "assets/gifts/diamond.png"},
    }

    def __init__(self, sender_username, recipient_username, user_coins, parent=None):
        super().__init__(parent)
        self.sender_username = sender_username
        self.recipient_username = recipient_username
        self.user_coins = user_coins  # dict like {'alice': 200, 'bob': 50}
        self.setWindowTitle("Send a Gift")
        self.setFixedSize(300, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        info_label = QLabel(
            f"Send a gift to {self.recipient_username}\nYour coins: {self.user_coins.get(self.sender_username, 0)}"
        )
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        self.gift_selector = QComboBox()
        for gift_name, gift_info in self.GIFTS.items():
            self.gift_selector.addItem(f"{gift_name} - {gift_info['cost']} coins", gift_info)
        layout.addWidget(self.gift_selector)

        send_btn = QPushButton("Send Gift")
        send_btn.setStyleSheet("background-color: #f0f0f0; color: black;")  # matte white button
        send_btn.clicked.connect(self.try_send_gift)
        layout.addWidget(send_btn)

        self.setLayout(layout)

    def try_send_gift(self):
        gift_info = self.gift_selector.currentData()
        gift_cost = gift_info["cost"]
        sender_balance = self.user_coins.get(self.sender_username, 0)

        if sender_balance < gift_cost:
            QMessageBox.warning(self, "Insufficient Coins", "You don't have enough coins to send this gift.")
            return

        self.user_coins[self.sender_username] -= gift_cost

        QMessageBox.information(self, "Gift Sent", f"You sent {self.gift_selector.currentText()}!")
        self.accept()

        if self.parent():
            gift_name = self.gift_selector.currentText().split(" - ")[0]
            self.parent().show_gift_animation(gift_name)


class GiftAnimationWidget(QWidget):
    def __init__(self, gift_name, parent=None):
        super().__init__(parent)
        self.gift_name = gift_name
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(150, 150)

        self.init_ui()
        self.animate()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.icon_label = QLabel("🎁")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setFont(QFont("Arial", 40))
        layout.addWidget(self.icon_label)

        self.label = QLabel(self.gift_name)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        self.label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(self.label)

        self.setLayout(layout)

    def animate(self):
        if self.parent():
            parent_geom = self.parent().geometry()
            start_x = parent_geom.x() + (parent_geom.width() - self.width()) // 2
            start_y = parent_geom.y() + parent_geom.height()
        else:
            start_x, start_y = 300, 600

        self.setGeometry(start_x, start_y, self.width(), self.height())
        self.show()

        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(3000)
        self.anim.setStartValue(QRect(start_x, start_y, self.width(), self.height()))
        self.anim.setEndValue(QRect(start_x, start_y - 200, self.width(), self.height()))
        self.anim.setEasingCurve(QEasingCurve.Type.OutBounce)
        self.anim.finished.connect(self.close)
        self.anim.start()


class GiftManager:
    def __init__(self, stream_window, user_coins):
        """
        :param stream_window: Reference to main StreamWindow for showing animations and notifications.
        :param user_coins: dict mapping username -> coin balance
        """
        self.stream_window = stream_window
        self.user_coins = user_coins
        self.gift_log = []

    def open_gift_dialog(self, sender_username, recipient_username):
        dlg = GiftDialog(sender_username, recipient_username, self.user_coins, parent=self.stream_window)
        result = dlg.exec()
        if result == QDialog.DialogCode.Accepted:
            gift_name = dlg.gift_selector.currentText().split(" - ")[0]
            self.gift_log.append({
                "sender": sender_username,
                "recipient": recipient_username,
                "gift": gift_name,
                "timestamp": QDateTime.currentDateTime(),
            })
            self.stream_window.show_gift_animation(gift_name)
            self.stream_window.show_gift_notification(sender_username, recipient_username, gift_name)

    def get_user_balance(self, username):
        return self.user_coins.get(username, 0)

    def add_coins(self, username, amount):
        self.user_coins[username] = self.user_coins.get(username, 0) + amount

    def get_gift_log(self):
        return self.gift_log
