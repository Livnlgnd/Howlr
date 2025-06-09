from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QScrollArea, QSizePolicy
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class DiscoverPage(QWidget):
    def __init__(self, users_online, follow_data=None):
        """
        users_online: list of usernames (str)
        follow_data: dict mapping username to set of usernames they follow, e.g.
                     {'current_user': {'userA', 'userB'}, 'userA': {...}, ...}
                     This is for managing follow state locally.
        """
        super().__init__()
        self.setWindowTitle("Discover Users")
        self.setGeometry(200, 100, 400, 600)

        self.users_online = users_online
        self.follow_data = follow_data if follow_data is not None else {}

        layout = QVBoxLayout(self)

        title = QLabel("Discover")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)

        self.scroll_area.setWidget(self.scroll_widget)
        layout.addWidget(self.scroll_area)

        self.refresh_users()

    def refresh_users(self):
        # Clear existing user cards
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Create user cards from the list
        for username in self.users_online:
            self.scroll_layout.addWidget(self._create_user_card(username))

    def _create_user_card(self, username):
        card = QWidget()
        layout = QHBoxLayout(card)

        # Profile picture (placeholder)
        profile_label = QLabel()
        pixmap = QPixmap("images/default.jpg")  # Use your default profile picture path
        pixmap = pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        profile_label.setPixmap(pixmap)
        layout.addWidget(profile_label)

        # User info
        info_layout = QVBoxLayout()
        name_label = QLabel(username)
        name_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        info_layout.addWidget(name_label)

        # Follow count display (followers and following)
        followers_count = self._count_followers(username)
        following_count = len(self.follow_data.get(username, set()))
        counts_label = QLabel(f"Followers: {followers_count}  Following: {following_count}")
        counts_label.setStyleSheet("font-size: 12px; color: gray;")
        info_layout.addWidget(counts_label)

        # Action buttons
        btn_layout = QHBoxLayout()

        message_btn = QPushButton("Message")
        join_btn = QPushButton("Join Stream")
        follow_btn = QPushButton()

        # Setup follow button text based on current user
        current_user = self.follow_data.get("current_user", "")
        if current_user and username != current_user:
            if username in self.follow_data.get(current_user, set()):
                follow_btn.setText("Unfollow")
            else:
                follow_btn.setText("Follow")
        else:
            follow_btn.setDisabled(True)  # Disable follow button for self or no user

        message_btn.clicked.connect(lambda _, u=username: self._message_user(u))
        join_btn.clicked.connect(lambda _, u=username: self._join_user_stream(u))
        follow_btn.clicked.connect(lambda _, u=username, btn=follow_btn: self._toggle_follow(u, btn))

        btn_layout.addWidget(message_btn)
        btn_layout.addWidget(join_btn)
        btn_layout.addWidget(follow_btn)
        info_layout.addLayout(btn_layout)

        layout.addLayout(info_layout)

        return card

    def _count_followers(self, username):
        count = 0
        for user, following_set in self.follow_data.items():
            if user == "current_user":
                continue
            if username in following_set:
                count += 1
        return count

    def _message_user(self, username):
        print(f"Opening chat with {username}...")  # Replace with actual messaging UI call

    def _join_user_stream(self, username):
        print(f"Joining {username}'s stream...")  # Replace with stream join logic

    def _toggle_follow(self, username, button):
        current_user = self.follow_data.get("current_user", None)
        if not current_user or username == current_user:
            return  # Can't follow self or no user

        following_set = self.follow_data.setdefault(current_user, set())

        if username in following_set:
            following_set.remove(username)
            button.setText("Follow")
            print(f"{current_user} unfollowed {username}")
        else:
            following_set.add(username)
            button.setText("Unfollow")
            print(f"{current_user} followed {username}")

        # Refresh to update follower/following counts
        self.refresh_users()
