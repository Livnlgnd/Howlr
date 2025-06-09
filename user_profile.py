from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class UserProfile(QWidget):
    def __init__(self, user_data, current_user_following, on_follow_change=None):
        """
        user_data: dict with keys like 'username', 'profile_picture', 'description', 'followers', 'following'
        current_user_following: list of usernames that current user follows
        on_follow_change: optional callback when follow status changes (username, followed: bool)
        """
        super().__init__()
        self.user_data = user_data
        self.current_user_following = current_user_following
        self.on_follow_change = on_follow_change

        self.setWindowTitle(f"Profile: {user_data['username']}")
        self.setGeometry(200, 200, 400, 500)

        self.layout = QVBoxLayout(self)

        # Profile Picture
        pixmap = QPixmap(user_data.get("profile_picture", "")).scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio)
        self.pic_label = QLabel()
        self.pic_label.setPixmap(pixmap)
        self.pic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.pic_label)

        # Username
        self.username_label = QLabel(user_data["username"])
        self.username_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.username_label)

        # Description
        self.description_label = QLabel(user_data.get("description", ""))
        self.description_label.setWordWrap(True)
        self.layout.addWidget(self.description_label)

        # Followers / Following count
        stats_layout = QHBoxLayout()
        self.followers_label = QLabel(f"Followers: {user_data.get('followers', 0)}")
        self.following_label = QLabel(f"Following: {user_data.get('following', 0)}")
        stats_layout.addWidget(self.followers_label)
        stats_layout.addWidget(self.following_label)
        self.layout.addLayout(stats_layout)

        # Follow / Unfollow button (hide if profile belongs to current user)
        self.follow_button = QPushButton()
        if user_data["username"] == "CurrentUser":  # Replace with actual current user check
            self.follow_button.setVisible(False)
        else:
            self._update_follow_button()
            self.follow_button.clicked.connect(self.toggle_follow)
            self.layout.addWidget(self.follow_button)

    def _update_follow_button(self):
        if self.user_data["username"] in self.current_user_following:
            self.follow_button.setText("Following")
        else:
            self.follow_button.setText("Follow")

    def toggle_follow(self):
        username = self.user_data["username"]
        if username in self.current_user_following:
            self.current_user_following.remove(username)
            # Optionally decrease follower count
            self.user_data['followers'] = max(0, self.user_data.get('followers', 1) - 1)
        else:
            self.current_user_following.append(username)
            # Optionally increase follower count
            self.user_data['followers'] = self.user_data.get('followers', 0) + 1

        self._update_follow_button()
        self.followers_label.setText(f"Followers: {self.user_data.get('followers', 0)}")

        if self.on_follow_change:
            self.on_follow_change(username, username in self.current_user_following)

        # TODO: Save changes locally or sync with backend if you have one
