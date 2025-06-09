from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import QTimer, Qt
from gift_manager import GiftManager
from gift_animation import GiftAnimationWidget

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

        # Label to show gift notifications
        self.gift_notification_label = QLabel("")
        self.gift_notification_label.setStyleSheet("color: yellow; font-weight: bold;")
        self.gift_notification_label.setVisible(False)

        # Button to open gifting dialog
        self.gift_button = QPushButton("Send Gift")
        self.gift_button.clicked.connect(self.open_gift_dialog)

        self.layout.addWidget(self.gift_button)
        self.layout.addWidget(self.gift_notification_label)

    def open_gift_dialog(self):
        # Call the gift manager's dialog
        self.gift_manager.open_gift_dialog(self.current_user, self.current_streamer_name)

    def show_gift_animation(self, gift_name):
        # Instantiate and show gift animation widget from external module
        anim = GiftAnimationWidget(gift_name, parent=self)
        anim.show()

    def show_gift_notification(self, sender, recipient, gift_name):
        text = f"{sender} sent {gift_name} to {recipient}!"
        self.gift_notification_label.setText(text)
        self.gift_notification_label.setVisible(True)
        QTimer.singleShot(5000, lambda: self.gift_notification_label.setVisible(False))
