# login_screen.py

import csv
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton,
    QMessageBox, QApplication, QSizePolicy, QHBoxLayout
)
from PyQt5.QtGui import QPalette, QLinearGradient, QColor, QBrush, QPixmap,QIcon
from PyQt5.QtCore import Qt

from config import COLOR_BACKGROUND_START, COLOR_BACKGROUND_END, COLOR_BUTTON_START, COLOR_BUTTON_END
from widgets import ShadowedTitle
# Import Menu here, but will handle circular import if needed in check_login by late import

class Login(QWidget):
    """
    Login/Register screen for the application.
    Dynamically sizes itself based on screen resolution and allows switching modes.
    """
    def __init__(self):
        super(Login, self).__init__()
        self.setWindowTitle("Physim-Login")
        self.setWindowIcon(QIcon('icons/atom.png'))

        # State to track current mode (Login or Register)
        self.is_register_mode = False

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
            logo_size = min(initial_width, initial_height) //5
            logo_icon.setPixmap(QPixmap('icons/atom.png').scaled(logo_size, logo_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
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

        self.title_widget = ShadowedTitle("Physim", parent=container) # Make title_widget an instance variable
        container_layout.addWidget(self.title_widget, alignment=Qt.AlignHCenter)
        layout.addWidget(container, alignment=Qt.AlignCenter)

        # Dynamic font sizes and padding for QLineEdit and QPushButton
        base_font_size = QApplication.font().pointSize() # Get the default font size
        line_edit_font_size = int(1.2 * base_font_size)
        line_edit_padding = int(1.0 * base_font_size)

        self.nim = QLineEdit()
        self.nim.setPlaceholderText("NIM")
        self.nim.setStyleSheet(f"font-size: {line_edit_font_size}px; padding: {line_edit_padding}px; border-radius: 10px; border: 2px solid #ccc;")
        self.nim.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.nim.setFixedWidth(int(initial_width * 0.7))
        layout.addWidget(self.nim, alignment=Qt.AlignHCenter)

        self.password = QLineEdit()
        self.password.setPlaceholderText("PASSWORD")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet(f"font-size: {line_edit_font_size}px; padding: {line_edit_padding}px; border-radius: 10px; border: 2px solid #ccc;")
        self.password.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.password.setFixedWidth(int(initial_width * 0.7))
        layout.addWidget(self.password, alignment=Qt.AlignHCenter)

        login_btn_font_size = int(1.5 * base_font_size)
        login_btn_padding_v = int(1.0 * base_font_size)
        login_btn_padding_h = int(2.0 * base_font_size)

        self.action_button = QPushButton("Login") # This button performs login or register
        self.action_button.setObjectName("ActionButton") # Set object name for findChild
        self.action_button.setStyleSheet(f"""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_BUTTON_START}, stop:1 {COLOR_BUTTON_END});
            color: white;
            padding: {login_btn_padding_v}px {login_btn_padding_h}px;
            font-size: {login_btn_font_size}px;
            font-weight: bold;
            border: none;
            border-radius: 20px;
        """)
        self.action_button.clicked.connect(self.perform_action)
        self.action_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.action_button.setFixedWidth(int(initial_width * 0.5))
        layout.addWidget(self.action_button, alignment=Qt.AlignCenter)

        # New button for toggling between login/register modes
        self.toggle_mode_button = QPushButton("Buat Akun Baru")
        self.toggle_mode_button.setObjectName("ToggleModeButton")
        toggle_btn_font_size = int(1.5 * base_font_size)
        self.toggle_mode_button.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: #1e3a8a;
                border: none;
                font-size: {toggle_btn_font_size}px;
                padding: 5px;
            }}
            QPushButton:hover {{
                text-decoration: underline;
            }}
        """)
        self.toggle_mode_button.clicked.connect(self.toggle_mode)
        layout.addWidget(self.toggle_mode_button, alignment=Qt.AlignCenter)


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
        
        action_button = self.findChild(QPushButton, "ActionButton")
        if action_button:
            action_button.setFixedWidth(int(current_width * 0.5)) 

        # Update logo size
        logo_icon = self.findChild(QLabel) # Assumes the first QLabel is the logo
        if logo_icon:
            logo_size = min(current_width, current_height) // 3
            logo_icon.setPixmap(QPixmap("icons/atom.png").scaled(logo_size, logo_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Update shadowed title size (handled by its own resizeEvent if parent is set correctly)
        self.title_widget._update_sizes() # Access directly if stored as instance variable


    def perform_action(self):
        """Performs login or registration based on current mode."""
        if self.is_register_mode:
            self.register_account()
        else:
            self.check_login()

    def toggle_mode(self):
        """Toggles between login and register modes."""
        self.is_register_mode = not self.is_register_mode
        self.nim.clear() # Clear fields when switching modes
        self.password.clear()

        if self.is_register_mode:
            self.setWindowTitle("Physim - Register")
            self.title_widget._title = "Registrasi" # Update internal title string
            self.title_widget._update_sizes() # Trigger title update
            self.action_button.setText("Registrasi")
            self.toggle_mode_button.setText("Sudah Punya Akun? Login")
        else:
            self.setWindowTitle("Physim-Login")
            self.title_widget._title = "Physim" # Reset internal title string
            self.title_widget._update_sizes() # Trigger title update
            self.action_button.setText("Login")
            self.toggle_mode_button.setText("Buat Akun Baru")

    def check_login(self):
        """Handles login attempt by checking credentials from CSV."""
        # Late import to prevent circular dependency
        from menu_screen import Menu 

        nim = self.nim.text()
        password = self.password.text()

        if not nim or not password:
            QMessageBox.warning(self, "Login Gagal", "NIM dan Password tidak boleh kosong.")
            return

        try:
            with open('source/Akun.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if nim == row['NIM'] and password == row['PASSWORD']:
                        self.menu = Menu(self)
                        self.menu.show()
                        self.hide()
                        return
                QMessageBox.warning(self, "Login Gagal", "NIM atau password salah.")
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "File 'source/Akun.csv' tidak ditemukan. Pastikan file ada di direktori yang benar.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan saat membaca file akun: {e}")

    def register_account(self):
        """Handles new account registration by saving credentials to CSV."""
        nim = self.nim.text()
        password = self.password.text()

        if not nim or not password:
            QMessageBox.warning(self, "Registrasi Gagal", "NIM dan Password tidak boleh kosong.")
            return

        # Check if NIM already exists
        nim_exists = False
        try:
            with open('source/Akun.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if nim == row['NIM']:
                        nim_exists = True
                        break
        except FileNotFoundError:
            # If file doesn't exist, it will be created, so NIM doesn't exist yet.
            pass
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan saat memeriksa NIM: {e}")
            return

        if nim_exists:
            QMessageBox.warning(self, "Registrasi Gagal", "NIM sudah terdaftar. Gunakan NIM lain atau Login.")
            return

        # Register new account
        try:
            # Open in append mode, 'a', and create file if it doesn't exist
            with open('source/Akun.csv', mode='a', newline='') as file:
                fieldnames = ['NIM', 'PASSWORD']
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                # Write header only if file is empty (newly created)
                if file.tell() == 0:
                    writer.writeheader()
                
                writer.writerow({'NIM': nim, 'PASSWORD': password})
            
            QMessageBox.information(self, "Registrasi Berhasil", "Akun berhasil dibuat! Silakan Login.")
            self.toggle_mode() # Switch back to login mode after successful registration
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan saat mendaftarkan akun: {e}")

