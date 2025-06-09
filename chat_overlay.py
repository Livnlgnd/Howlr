# chat_overlay.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer

class ChatOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setStyleSheet("background: transparent;")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def show_message(self, msg):
        label = QLabel(msg)
        label.setStyleSheet("color: white; font-size: 16px;")
        label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(label)

        # Remove after 5 seconds
        QTimer.singleShot(5000, lambda: self.layout.removeWidget(label) or label.deleteLater())
