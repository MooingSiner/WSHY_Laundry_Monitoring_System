from PyQt6.QtWidgets import QWidget, QLabel, QApplication, QPushButton, QLineEdit
from PyQt6.QtGui import QPainter, QPixmap, QFont, QFontDatabase, QIcon
from PyQt6.QtCore import Qt
import os


class LoginView(QWidget):
    def __init__(self, image="images/1.png", base_path=""):
        super().__init__()
        self.image = QPixmap(image)
        self.base_path = base_path
        self.password_visible = False

        # Set window title
        self.setWindowTitle("Login")

        # Logo
        icon = QLabel(self)
        logo_path = os.path.join(base_path, "images/LOGO.png")
        icon.setPixmap(QPixmap(logo_path).scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio,
                                                 Qt.TransformationMode.SmoothTransformation))
        icon.setGeometry(450, 120, 120, 120)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Washy Title
        label = QLabel("Washy", self)
        label.setGeometry(0, 250, 1024, 60)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Load custom font
        font_path = os.path.join(base_path, "fonts/Fredoka-SemiBold.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            family = "Arial"  # Fallback font

        label.setFont(QFont(family, 36, QFont.Weight.Bold))
        label.setStyleSheet("color: #1a1a1a;")

        # USERNAME INPUT FIELD
        self.username = QLineEdit(self)
        self.username.setPlaceholderText("Username")
        self.username.setGeometry(362, 340, 300, 50)
        self.username.setStyleSheet("""
            QLineEdit {
                background: #e8e8e8;
                border: 2px solid #d0d0d0;
                border-radius: 15px;
                padding-left: 15px;
                padding-right: 15px;
                font-size: 15px;
                color: #333;
            }
            QLineEdit:focus {
                border: 2px solid #3855DB;
                background: #f5f5f5;
            }
        """)

        # PASSWORD INPUT FIELD
        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setGeometry(362, 405, 300, 50)
        self.password.setStyleSheet("""
            QLineEdit {
                background: #e8e8e8;
                border: 2px solid #d0d0d0;
                border-radius: 15px;
                padding-left: 15px;
                padding-right: 50px;
                font-size: 15px;
                color: #333;
            }
            QLineEdit:focus {
                border: 2px solid #3855DB;
                background: #f5f5f5;
            }
        """)

        # SHOW/HIDE PASSWORD BUTTON
        self.show_password_btn = QPushButton("Show", self)
        self.show_password_btn.setGeometry(610, 415, 45, 30)
        self.show_password_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.show_password_btn.setFont(QFont(family, 9))
        self.show_password_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #3855DB;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #2746C3;
            }
        """)
        self.show_password_btn.clicked.connect(self.toggle_password_visibility)

        # LOGIN BUTTON
        self.login_btn = QPushButton("Login", self)
        self.login_btn.setFont(QFont(family, 16, QFont.Weight.Bold))
        self.login_btn.setGeometry(412, 480, 200, 50)
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #3855DB;
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2746C3;
            }
            QPushButton:pressed {
                background-color: #1a3399;
            }
        """)

    def toggle_password_visibility(self):
        if self.password_visible:
            self.password.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_password_btn.setText("Show")
            self.password_visible = False
        else:
            self.password.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_password_btn.setText("Hide")
            self.password_visible = True

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.width(), self.height(), self.image)
        painter.end()