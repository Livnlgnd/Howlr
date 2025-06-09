from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import QTimer, QPropertyAnimation, QPoint, QEasingCurve, Qt
from PyQt6.QtGui import QFont, QColor, QPainter, QPainterPath

class GiftAnimationWidget(QWidget):
    def __init__(self, gift_name, parent=None):
        super().__init__(parent)
        self.gift_name = gift_name
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(200, 50)

        self.label = QLabel(self.gift_name, self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(0, 0, 200, 50)
        font = QFont("Arial", 16, QFont.Weight.Bold)
        self.label.setFont(font)
        self.label.setStyleSheet("color: gold; background-color: rgba(0,0,0,150); border-radius: 10px;")

        self.start_animation()

    def start_animation(self):
        # Start position: bottom center of parent or screen
        if self.parent():
            parent_rect = self.parent().geometry()
            start_x = parent_rect.x() + parent_rect.width() // 2 - self.width() // 2
            start_y = parent_rect.y() + parent_rect.height() - self.height() - 20
        else:
            screen = self.screen()
            rect = screen.availableGeometry()
            start_x = rect.center().x() - self.width() // 2
            start_y = rect.bottom() - self.height() - 50

        self.move(start_x, start_y)

        # Animation: move up and fade out
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(3000)
        self.anim.setStartValue(QPoint(start_x, start_y))
        self.anim.setEndValue(QPoint(start_x, start_y - 150))
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_anim.setDuration(3000)
        self.opacity_anim.setStartValue(1)
        self.opacity_anim.setEndValue(0)

        # When animation finishes, close the widget
        self.opacity_anim.finished.connect(self.close)

        # Start animations
        self.anim.start()
        self.opacity_anim.start()
