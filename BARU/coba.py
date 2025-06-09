import sys
import pygame
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton,
    QMainWindow, QMessageBox, QGridLayout, QAction, QSizePolicy, QFrame, QSlider, QHBoxLayout
)
from PyQt5.QtGui import QFont, QPalette, QLinearGradient, QColor, QBrush, QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer
from glbb import GLBBSimulation

class PygameEmbedWidget(QLabel):
    def __init__(self, simulation, width, height, parent=None):
        super().__init__(parent)
        self.setFixedSize(width, height)
        self.simulation = simulation

    def update_display(self):
        surface = self.simulation.surface
        raw_str = pygame.image.tostring(surface, "RGBA")
        qimage = QImage(raw_str, surface.get_width(), surface.get_height(), QImage.Format_RGBA8888)
        self.setPixmap(QPixmap.fromImage(qimage))

class LoginScreen(QWidget):
    def __init__(self):
        super(LoginScreen, self).__init__()
        self.setWindowTitle("Physim-Login")
        self.setMinimumSize(400, 300)

        # Background gradient
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 800, 600)
        gradient.setColorAt(0.0, QColor("#a2d4f5"))
        gradient.setColorAt(1.0, QColor("#ffffff"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        layout = QVBoxLayout()

        # Logo
        logo_layout = QVBoxLayout()
        logo_icon = QLabel()
        logo_icon.setPixmap(QPixmap("icons/atom.png").scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_icon.setAlignment(Qt.AlignCenter)
        logo_title = QLabel("Physim")
        logo_title.setFont(QFont("Arial", 36, QFont.Bold))
        logo_title.setAlignment(Qt.AlignCenter)
        logo_title.setStyleSheet("color: #1e3a8a;")
        logo_layout.addWidget(logo_icon)
        logo_layout.addWidget(logo_title)
        layout.addLayout(logo_layout)

        self.nim = QLineEdit()
        self.nim.setPlaceholderText("NIM")
        self.nim.setStyleSheet("font-size: 16px; padding: 12px; border-radius: 10px; border: 2px solid #ccc;")
        layout.addWidget(self.nim)

        self.password = QLineEdit()
        self.password.setPlaceholderText("PASSWORD")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet("font-size: 16px; padding: 12px; border-radius: 10px; border: 2px solid #ccc;")
        layout.addWidget(self.password)

        login_btn = QPushButton("Login")
        login_btn.setStyleSheet("""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #7aa0ff, stop:1 #5e60ce);
            color: white;
            padding: 12px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            border-radius: 20px;
        """)
        login_btn.clicked.connect(self.check_login)
        layout.addWidget(login_btn, alignment=Qt.AlignCenter)

        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(10)
        self.setLayout(layout)

    def check_login(self):
        if self.nim.text() == "H1A024xxx" and self.password.text() == "kel20":
            self.menu = Menu(self)
            self.menu.show()
            self.hide()
        else:
            QMessageBox.warning(self, "Login Failed", "NIM atau password salah.")

class BaseTopicScreen(QMainWindow):
    def __init__(self, menu_window, title):
        super(BaseTopicScreen, self).__init__()
        self.menu_window = menu_window
        self.setWindowTitle(title)
        self.resize(800, 600)
        
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 800, 600)
        gradient.setColorAt(0.0, QColor("#a2d4f5"))
        gradient.setColorAt(1.0, QColor("#ffffff"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Central widget
        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.main_layout = QVBoxLayout()
        self.central.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(20)

        # Header label
        header = QLabel(title)
        header.setStyleSheet("color: #111111; font-weight: 800; font-size: 36px;")
        header.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(header)

        # Content label that subclasses can customize
        self.content_label = QLabel()
        self.content_label.setStyleSheet("color: #6b7280; font-size: 18px; line-height: 1.4;")
        self.content_label.setAlignment(Qt.AlignCenter)
        self.content_label.setWordWrap(True)
        self.main_layout.addWidget(self.content_label, alignment=Qt.AlignTop)

        # Spacer frame (flexible space)
        spacer = QFrame()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_layout.addWidget(spacer)

        # Back to Menu button
        back_btn = QPushButton("← Kembali ke Menu")
        back_btn.setStyleSheet("""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #7aa0ff, stop:1 #5e60ce);
            color: white;
            padding: 12px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            border-radius: 20px;
        """)
        back_btn.clicked.connect(self.back_to_menu)
        self.main_layout.addWidget(back_btn, alignment=Qt.AlignBottom)

        # Menu bar (sticky)
        self.menu_bar = self.menuBar()
        self.menu_bar.setStyleSheet("""
            QMenuBar {
                background-color: #ffffff;
                font-weight: 600;
                font-size: 14px;
                color: #111111;
            }
            QMenuBar::item {
                spacing: 6px;
                padding: 6px 12px;
                background: transparent;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background: #e2e8f0;
            }
            QMenu {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
            }
            QMenu::item:selected {
                background-color: #cbd5e1;
                color: #111111;
            }
        """)

        account_menu = self.menu_bar.addMenu("Akun")
        logout_action = QAction("← Logout", self)
        account_menu.addAction(logout_action)
        logout_action.triggered.connect(self.logout)

    def _set_content_text(self, text: str):
        self.content_label.setText(text)

    def back_to_menu(self):
        self.menu_window.show()
        self.close()

    def logout(self):
        self.menu_window.login_window.show()
        self.menu_window.close()  # Close menu window
        self.close()

class GerakLurusScreen(BaseTopicScreen):
    def __init__(self, menu_window):
        super(GerakLurusScreen, self).__init__(menu_window, "Gerak Lurus")
        self.simulation = GLBBSimulation(width=800, height=400)
        self.pygame_widget = PygameEmbedWidget(self.simulation, 800, 400)

        # Wrap pygame_widget in horizontal layout to center it
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.pygame_widget)
        hbox.addStretch()
        self.main_layout.addLayout(hbox)

        self.slider_label = QLabel("Akselerasi: 0.00 m/s²")
        self.slider_label.setAlignment(Qt.AlignCenter)
        self.slider_label.setFont(QFont("Arial", 12))
        self.main_layout.addWidget(self.slider_label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(-5000, 5000)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.update_acceleration)
        self.main_layout.addWidget(self.slider)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.game_tick)
        self.timer.start(1000 // 60)

    def update_acceleration(self, value):
        accel_value = value / 100.0
        self.simulation.set_acceleration(accel_value)
        self.slider_label.setText(f"Akselerasi: {accel_value:.2f} m/s²")

    def game_tick(self):
        self.simulation.step()
        self.simulation.draw()
        self.pygame_widget.update_display()

class HukumNewtonScreen(BaseTopicScreen):
    def __init__(self, menu_window):
        super(HukumNewtonScreen, self).__init__(menu_window, "Hukum Newton")
        self._set_content_text("Penjelasan mengenai hukum Newton akan ditampilkan di sini.")

class HukumHookeScreen(BaseTopicScreen):
    def __init__(self, menu_window):
        super(HukumHookeScreen, self).__init__(menu_window, "Hukum Hooke")
        self._set_content_text("Penjelasan mengenai hukum Hooke akan ditampilkan di sini.")

class RangkaianResistorScreen(BaseTopicScreen):
    def __init__(self, menu_window):
        super(RangkaianResistorScreen, self).__init__(menu_window, "Rangkaian Resistor")
        self._set_content_text("Simulasi rangkaian resistor akan ditampilkan di sini.")

class GerakHarmonikScreen(BaseTopicScreen):
    def __init__(self, menu_window):
        super(GerakHarmonikScreen, self).__init__(menu_window, "Gerak Harmonik")
        self._set_content_text("Simulasi gerak harmonik sederhana akan ditampilkan di sini.")

class HukumArchimedesScreen(BaseTopicScreen):
    def __init__(self, menu_window):
        super(HukumArchimedesScreen, self).__init__(menu_window, "Hukum Archimedes")
        self._set_content_text("Penjelasan tentang hukum Archimedes akan ditampilkan di sini.")

class Menu(QMainWindow):
    def __init__(self, login_window):
        super(Menu, self).__init__()
        self.login_window = login_window
        self.setWindowTitle("PhySim - Menu")
        self.resize(800, 600)

        # Menu bar
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #f9f9f9;
                font-weight: 600;
                font-size: 14px;
                color: #111111;
            }
            QMenuBar::item {
                spacing: 6px;
                padding: 6px 12px;
                background: transparent;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background: #e2e8f0;
            }
            QMenu {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
            }
            QMenu::item:selected {
                background-color: #cbd5e1;
                color: #111111;
            }
        """)
        account_menu = menubar.addMenu("Akun")
        logout_action = QAction("← Logout", self)
        account_menu.addAction(logout_action)
        logout_action.triggered.connect(self.handle_logout)

        # Background gradient
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 800, 600)
        gradient.setColorAt(0.0, QColor("#a2d4f5"))
        gradient.setColorAt(1.0, QColor("#ffffff"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Title label
        title_label = QLabel("PILIH MATERI")
        title_font = QFont("Arial", 32, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        main_layout.addWidget(title_label)

        button_grid = QGridLayout()
        buttons = []

        simulasi_labels = ["Gerak Lurus", "Hukum Newton", "Hukum Hooke", "Rangkaian Resistor", "Gerak Harmonik", "Hukum Archimedes"]

        for i in range(6):
            icon_path = f"icons/{i + 1}.png"
            btn = QPushButton()
            btn.setMinimumSize(100, 100)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setStyleSheet(f"""
                               QPushButton {{
                               background-image: url({icon_path});
                               background-position: center;
                               background-repeat: no-repeat;
                               background-color: white;
                               border: 1px solid #aaa;
                               border-radius: 8px;}}
                               QPushButton:hover {{
                               border-color: #0078d4;
                               box-shadow: 0 0 8px rgba(0,120,212,0.6);
                               }}
                               """)
            buttons.append(btn)
            btn.clicked.connect(lambda checked, index=i: self.open_screen(index))

            label = QLabel(simulasi_labels[i])
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: black; font-weight: bold; font-size: 14px;")

            vbox = QVBoxLayout()
            vbox.addWidget(btn)
            vbox.addWidget(label)
            container = QWidget()
            container.setLayout(vbox)

            button_grid.addWidget(container, i // 3, i % 3)

        main_layout.addLayout(button_grid)

    def open_screen(self, index):
        # Hide menu when opening a new screen
        self.hide()
        if index == 0:
            self.screen = GerakLurusScreen(self)
        elif index == 1:
            self.screen = HukumNewtonScreen(self)
        elif index == 2:
            self.screen = HukumHookeScreen(self)
        elif index == 3:
            self.screen = RangkaianResistorScreen(self)
        elif index == 4:
            self.screen = GerakHarmonikScreen(self)
        elif index == 5:
            self.screen = HukumArchimedesScreen(self)
        else:
            return
        self.screen.show()

    def handle_logout(self):
        self.login_window.show()
        self.close()

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    login_window = LoginScreen()
    login_window.show()
    sys.exit(app.exec_())

