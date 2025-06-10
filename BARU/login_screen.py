# login_screen.py

import csv
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton,
    QMessageBox, QApplication, QSizePolicy
)
from PyQt5.QtGui import QPalette, QLinearGradient, QColor, QBrush, QPixmap
from PyQt5.QtCore import Qt

from config import COLOR_BACKGROUND_START, COLOR_BACKGROUND_END, COLOR_BUTTON_START, COLOR_BUTTON_END
from widgets import ShadowedTitle
from menu_screen import Menu # Import Menu here (circular import will be handled by late import in check_login)

class Login(QWidget):
    """
    Login screen for the application.
    Dynamically sizes itself based on screen resolution.
    """
    def __init__(self):
        super(Login, self).__init__()
        self.setWindowTitle("Physim-Login")

        # Get primary screen geometry
        screen_rect = QApplication.primaryScreen().geometry()
        # Set initial window size to a percentage of screen size
        initial_width = int(screen_rect.width() * 0.4)
        initial_height = int(screen_rect.height() * 0.5)
        self.resize(initial_width, initial_height)
        self.setMinimumSize(int(initial_width * 0.7), int(initial_height * 0.7)) # Set a flexible minimum size

        # Background gradient
        palette = QPalette()
        gradient = QLinearGradient(0, 0, screen_rect.width(), screen_rect.height())
        gradient.setColorAt(0.0, QColor(COLOR_BACKGROUND_START))
        gradient.setColorAt(1.0, QColor(COLOR_BACKGROUND_END))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        layout = QVBoxLayout()
        layout.addStretch(1) # Add flexible space at the top

        logo_icon = QLabel()
        try:
            # Scale logo size based on initial window size, e.g., 1/3 of the smaller dimension
            logo_size = min(initial_width, initial_height) // 3
            logo_icon.setPixmap(QPixmap("icons/atom.png").scaled(logo_size, logo_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except Exception as e:
            print(f"Error loading logo: {e}")
        logo_icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_icon, alignment=Qt.AlignCenter)

        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setSpacing(int(initial_height * 0.05)) # Dynamic spacing
        container_layout.setContentsMargins(0,0,0,0)
        container.setLayout(container_layout)
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        title_widget = ShadowedTitle("Physim", parent=container) # Pass container as parent
        container_layout.addWidget(title_widget, alignment=Qt.AlignHCenter)
        layout.addWidget(container, alignment=Qt.AlignCenter)

        # Dynamic font sizes and padding for QLineEdit and QPushButton
        base_font_size = QApplication.font().pointSize() # Get the default font size
        line_edit_font_size = int(1.2 * base_font_size)
        line_edit_padding = int(1.0 * base_font_size)

        self.nim = QLineEdit()
        self.nim.setPlaceholderText("NIM")
        self.nim.setStyleSheet(f"font-size: {line_edit_font_size}px; padding: {line_edit_padding}px; border-radius: 10px; border: 2px solid #ccc;")
        self.nim.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed) # Keep height fixed, allow width to expand
        self.nim.setFixedWidth(int(initial_width * 0.7)) # Set initial width based on window size
        layout.addWidget(self.nim, alignment=Qt.AlignHCenter)

        self.password = QLineEdit()
        self.password.setPlaceholderText("PASSWORD")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet(f"font-size: {line_edit_font_size}px; padding: {line_edit_padding}px; border-radius: 10px; border: 2px solid #ccc;")
        self.password.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.password.setFixedWidth(int(initial_width * 0.7)) # Set initial width based on window size
        layout.addWidget(self.password, alignment=Qt.AlignHCenter)

        login_btn_font_size = int(1.5 * base_font_size)
        login_btn_padding_v = int(1.0 * base_font_size)
        login_btn_padding_h = int(2.0 * base_font_size)

        login_btn = QPushButton("Login")
        login_btn.setObjectName("Login") # Set the object name for findChild to work
        login_btn.setStyleSheet(f"""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_BUTTON_START}, stop:1 {COLOR_BUTTON_END});
            color: white;
            padding: {login_btn_padding_v}px {login_btn_padding_h}px;
            font-size: {login_btn_font_size}px;
            font-weight: bold;
            border: none;
            border-radius: 20px;
        """)
        login_btn.clicked.connect(self.check_login)
        login_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed) # Fixed size, but centrally aligned
        login_btn.setFixedWidth(int(initial_width * 0.5)) # Set initial width based on window size
        layout.addWidget(login_btn, alignment=Qt.AlignCenter)

        layout.addStretch(1) # Add flexible space at the bottom

        # Dynamic margins based on initial window size
        layout.setContentsMargins(int(initial_width * 0.1), int(initial_height * 0.08), int(initial_width * 0.1), int(initial_height * 0.08))
        layout.setSpacing(int(initial_height * 0.02)) # Dynamic spacing
        self.setLayout(layout)

        # Override resizeEvent for Login to dynamically adjust sizes
        self.resizeEvent = self.login_resizeEvent

    def login_resizeEvent(self, event):
        """Handle resize events to update sizes of elements in Login screen."""
        super().resizeEvent(event)
        current_width = self.width()
        current_height = self.height()

        # Update line edit and button widths
        self.nim.setFixedWidth(int(current_width * 0.7))
        self.password.setFixedWidth(int(current_width * 0.7))
        
        login_button = self.findChild(QPushButton, "Login") # Find login_btn by object name
        if login_button: # Check if the button was found
            login_button.setFixedWidth(int(current_width * 0.5)) 

        # Update logo size
        logo_icon = self.findChild(QLabel) # Assumes the first QLabel is the logo
        if logo_icon:
            logo_size = min(current_width, current_height) // 3
            logo_icon.setPixmap(QPixmap("icons/atom.png").scaled(logo_size, logo_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Update shadowed title size (handled by its own resizeEvent if parent is set correctly)
        self.findChild(ShadowedTitle)._update_sizes() # Manually trigger update if needed


    def check_login(self):
        """Handles login attempt by checking credentials from CSV."""
        # Late import to prevent circular dependency
        from menu_screen import Menu 

        try:
            with open('source/Akun.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if self.nim.text() == row['NIM'] and self.password.text() == row['PASSWORD']:
                        self.menu = Menu(self)
                        self.menu.show()
                        self.hide()
                        return
                QMessageBox.warning(self, "Login Failed", "NIM atau password salah.")
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "File 'source/Akun.csv' tidak ditemukan. Pastikan file ada di direktori yang benar.")

