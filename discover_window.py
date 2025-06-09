from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea, QFrame
from PyQt6.QtCore import Qt
from stream_window import StreamWindow
from user_utils import load_users  # Assuming your user loading is in user_utils.py
from home_screen import HomeScreen

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
        self.stream_window = StreamWindow(self.current_user, username)
        self.stream_window.show()

    def back_to_home(self):
        self.close()
        self.home = HomeScreen(self.current_user)
        self.home.show()
