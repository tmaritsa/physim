import sys
import csv
import pygame
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton,
    QMainWindow, QMessageBox, QGridLayout, QAction, QSizePolicy, QFrame, QSlider, QHBoxLayout, QTextEdit, QSpacerItem
)
from PyQt5.QtGui import QFont, QPalette, QLinearGradient, QColor, QBrush, QPixmap, QImage, QFontMetrics
from PyQt5.QtCore import Qt, QTimer
from glbb import GLBBSimulation

# Constants for colors
COLOR_BACKGROUND_START = "#a2d4f5"
COLOR_BACKGROUND_END = "#ffffff"
COLOR_TEXT = "#1e3a8a"
COLOR_BUTTON_START = "#7aa0ff"
COLOR_BUTTON_END = "#5e60ce"
COLOR_ERROR_TEXT = "#111111"

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

class ShadowedTitle(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        font = QFont("Sans Serif", 48, QFont.ExtraBold)
        fm = QFontMetrics(font)
        text_width = fm.horizontalAdvance(title)
        text_height = fm.height()
        padding = 12
        
        self.setFixedSize(text_width + padding * 2 + 6, text_height + padding * 2 + 6)
        self.shadow1 = QLabel(title, self)
        self.shadow1.setFont(font)
        self.shadow1.setStyleSheet("color: #93c5fd;")
        self.shadow1.move(padding + 6, padding + 6)
        self.shadow1.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.shadow2 = QLabel(title, self)
        self.shadow2.setFont(font)
        self.shadow2.setStyleSheet("color: #1e40af;")
        self.shadow2.move(padding + 3, padding + 3)
        self.shadow2.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.main_text = QLabel(title, self)
        self.main_text.setFont(font)
        self.main_text.setStyleSheet("color: white;")
        self.main_text.move(padding, padding)
        self.main_text.setAttribute(Qt.WA_TransparentForMouseEvents)

class Login(QWidget):
    def __init__(self):
        super(Login, self).__init__()
        self.setWindowTitle("Physim-Login")
        self.setMinimumSize(400, 300)

        # Background gradient
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 800, 600)
        gradient.setColorAt(0.0, QColor(COLOR_BACKGROUND_START))
        gradient.setColorAt(1.0, QColor(COLOR_BACKGROUND_END))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        layout = QVBoxLayout()

        logo_icon = QLabel()
        try:
            logo_icon.setPixmap(QPixmap("icons/atom.png").scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except Exception as e:
            print(f"Error loading logo: {e}")
        logo_icon.setAlignment(Qt.AlignCenter)
        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setSpacing(24)
        container_layout.setContentsMargins(0,0,0,0)
        container.setLayout(container_layout)
        container.setMaximumWidth(480)
        title_widget = ShadowedTitle("Physim")
        container_layout.addWidget(title_widget, alignment=Qt.AlignHCenter)
        layout.addWidget(logo_icon)
        layout.addWidget(container, alignment=Qt.AlignCenter)

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
        login_btn.setStyleSheet(f"""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_BUTTON_START}, stop:1 {COLOR_BUTTON_END});
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
        with open('source/Akun.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if self.nim.text() == row['NIM'] and self.password.text() == row['PASSWORD']:
                    self.menu = Menu(self)
                    self.menu.show()
                    self.hide()
                    return
            QMessageBox.warning(self, "Login Failed", "NIM atau password salah.")

class Materi(QMainWindow):
    def __init__(self, menu_window, title):
        super(Materi, self).__init__()
        self.menu_window = menu_window
        self.setWindowTitle(title)
        self.resize(800, 600)
        
        # Background gradient
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 800, 600)
        gradient.setColorAt(0.0, QColor(COLOR_BACKGROUND_START))
        gradient.setColorAt(1.0, QColor(COLOR_BACKGROUND_END))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Central widget
        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.main_layout = QVBoxLayout()
        self.central.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(0)

        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setSpacing(0)
        container_layout.setContentsMargins(0,0,0,0)
        container.setLayout(container_layout)
        container.setMaximumWidth(900)
        title_widget = ShadowedTitle(title)
        container_layout.addWidget(title_widget, alignment=Qt.AlignHCenter)
        self.main_layout.addWidget(container, alignment=Qt.AlignCenter)

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

        # Back to Menu button placeholder (in subclasses)

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
        logout_action = QAction("Logout", self)
        account_menu.addAction(logout_action)
        logout_action.triggered.connect(self.logout)

    def _set_content_text(self, text: str):
        self.content_label.setText(text)
        pass

    def back_to_menu(self):
        self.menu_window.show()
        self.close()

    def logout(self):
        self.menu_window.login_window.show()
        self.menu_window.close()  # Close menu window
        self.close()

class GL(Materi):
    def __init__(self, menu_window):
        super(GL, self).__init__(menu_window, "Gerak Lurus")
        self.simulation = GLBBSimulation(width=800, height=400)
        self.pygame_widget = PygameEmbedWidget(self.simulation, 800, 400)
        self.kuis_screen = Kuis(self)

        # Wrap pygame_widget in horizontal layout to center and raise its vertical position
        hbox_sim = QHBoxLayout()
        hbox_sim.addStretch()
        hbox_sim.addWidget(self.pygame_widget)
        hbox_sim.addStretch()

        # Add top margin to raise simulation widget visually
        container_sim = QWidget()
        vbox_container = QVBoxLayout()
        vbox_container.setContentsMargins(0, 0, 0, 0)  # 24px top margin to raise it
        vbox_container.addLayout(hbox_sim)
        container_sim.setLayout(vbox_container)
        self.main_layout.addWidget(container_sim)

        self.slider_label = QLabel("Akselerasi: 0.00 m/s²")
        self.slider_label.setAlignment(Qt.AlignCenter)
        self.slider_label.setFont(QFont("Arial", 12))
        self.main_layout.addWidget(self.slider_label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(-5000, 5000)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.update_acceleration)
        self.slider.setFixedWidth(800)
        self.slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border-radius: 8px;
                height: 12px;
                background: #e0e2e7;
            }
            QSlider::handle:horizontal {
                background: #3b82f6;
                border-radius: 12px;
                width: 28px;
                margin: -8px 0;
                transition: background-color 0.3s ease;
            }
            QSlider::handle:horizontal:hover {
                background: #2563eb;
            }
            QSlider::sub-page:horizontal {
                background: #3b82f6;
                border-radius: 8px;
            }
            QSlider::add-page:horizontal {
                background: #e0e2e7;
                border-radius: 8px;
            }
        """)

        # Put slider inside horizontal layout for centered expansion
        slider_layout = QHBoxLayout()
        slider_layout.setContentsMargins(0, 0, 0, 0)
        slider_layout.addStretch()
        slider_layout.addWidget(self.slider)
        slider_layout.addStretch()
        self.main_layout.addLayout(slider_layout)

        # Buttons for Menu and Kuis in layout constrained by max width
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        back_btn = QPushButton("Menu")
        back_btn.setStyleSheet(f"""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_BUTTON_START}, stop:1 {COLOR_BUTTON_END});
            color: white;
            padding: 12px 24px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            border-radius: 20px;
        """)
        back_btn.clicked.connect(self.back_to_menu)
        button_layout.addWidget(back_btn)

        kuis_btn = QPushButton("Kuis")
        kuis_btn.setStyleSheet(f"""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_BUTTON_START}, stop:1 {COLOR_BUTTON_END});
            color: white;
            padding: 12px 24px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            border-radius: 20px;
        """)
        kuis_btn.clicked.connect(self.gokuis)
        button_layout.addWidget(kuis_btn)

        button_layout.addStretch()

        button_container = QWidget()
        button_container.setLayout(button_layout)
        button_container.setMaximumWidth(480)  # Constrain buttons to page width approx
        self.main_layout.addWidget(button_container)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.game_tick)
        self.timer.start(1000 // 60)

    def gokuis(self):
        self.kuis_screen.show()
        self.close()

    def update_acceleration(self, value):
        accel_value = value / 100.0
        self.simulation.set_acceleration(accel_value)
        self.slider_label.setText(f"Akselerasi: {accel_value:.2f} m/s²")

    def game_tick(self):
        self.simulation.step()
        self.simulation.draw()
        self.pygame_widget.update_display()

class Newton(Materi):
    def __init__(self, menu_window):
        super(Newton, self).__init__(menu_window, "Hukum Newton")
        self._set_content_text("Penjelasan mengenai hukum Newton akan ditampilkan di sini.")
        back_btn = QPushButton("Menu")
        back_btn.setStyleSheet(f"""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_BUTTON_START}, stop:1 {COLOR_BUTTON_END});
            color: white;
            padding: 12px 24px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            border-radius: 20px;
        """)
        back_btn.clicked.connect(self.back_to_menu)
        self.main_layout.addWidget(back_btn)

class Hooke(Materi):
    def __init__(self, menu_window):
        super(Hooke, self).__init__(menu_window, "Hukum Hooke")
        self._set_content_text("Penjelasan mengenai hukum Hooke akan ditampilkan di sini.")
        back_btn = QPushButton("Menu")
        back_btn.setStyleSheet(f"""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_BUTTON_START}, stop:1 {COLOR_BUTTON_END});
            color: white;
            padding: 12px 24px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            border-radius: 20px;
        """)
        back_btn.clicked.connect(self.back_to_menu)
        self.main_layout.addWidget(back_btn)



class Resistor(Materi):
    def __init__(self, menu_window):
        super(Resistor, self).__init__(menu_window, "Rangkaian Resistor")
        self._set_content_text("Simulasi rangkaian resistor akan ditampilkan di sini.")
        back_btn = QPushButton("Menu")
        back_btn.setStyleSheet(f"""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_BUTTON_START}, stop:1 {COLOR_BUTTON_END});
            color: white;
            padding: 12px 24px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            border-radius: 20px;
        """)
        back_btn.clicked.connect(self.back_to_menu)
        self.main_layout.addWidget(back_btn)


class Bandul(Materi):
    def __init__(self, menu_window):
        super(Bandul, self).__init__(menu_window, "Gerak Harmonik")
        self._set_content_text("Simulasi gerak harmonik sederhana akan ditampilkan di sini.")
        back_btn = QPushButton("Menu")
        back_btn.setStyleSheet(f"""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_BUTTON_START}, stop:1 {COLOR_BUTTON_END});
            color: white;
            padding: 12px 24px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            border-radius: 20px;
        """)
        back_btn.clicked.connect(self.back_to_menu)
        self.main_layout.addWidget(back_btn)


class Archimedes(Materi):
    def __init__(self, menu_window):
        super(Archimedes, self).__init__(menu_window, "Hukum Archimedes")
        self._set_content_text("Penjelasan tentang hukum Archimedes akan ditampilkan di sini.")
        back_btn = QPushButton("Menu")
        back_btn.setStyleSheet(f"""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_BUTTON_START}, stop:1 {COLOR_BUTTON_END});
            color: white;
            padding: 12px 24px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            border-radius: 20px;
        """)
        back_btn.clicked.connect(self.back_to_menu)
        self.main_layout.addWidget(back_btn)


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
        logout_action = QAction("Logout", self)
        account_menu.addAction(logout_action)
        logout_action.triggered.connect(self.handle_logout)

        # Background gradient
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 800, 600)
        gradient.setColorAt(0.0, QColor(COLOR_BACKGROUND_START))
        gradient.setColorAt(1.0, QColor(COLOR_BACKGROUND_END))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setSpacing(24)
        container_layout.setContentsMargins(0,0,0,0)
        container.setLayout(container_layout)
        container.setMaximumWidth(480)
        title_widget = ShadowedTitle("Pilih Materi")
        container_layout.addWidget(title_widget, alignment=Qt.AlignHCenter)
        main_layout.addWidget(container, alignment=Qt.AlignCenter)

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
            self.screen = GL(self)
        elif index == 1:
            self.screen = Newton(self)
        elif index == 2:
            self.screen = Hooke(self)
        elif index == 3:
            self.screen = Resistor(self)
        elif index == 4:
            self.screen = Bandul(self)
        elif index == 5:
            self.screen = Archimedes(self)
        else:
            return
        self.screen.show()

    def handle_logout(self):
        self.login_window.show()
        self.close()

class Kuis(QMainWindow):
    def __init__(self, menu_window):
        super().__init__()
        self.menu_window = menu_window
        self.setWindowTitle("Kuis")
        self.resize(820, 600)

        # Background gradient
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 800, 600)
        gradient.setColorAt(0.0, QColor(COLOR_BACKGROUND_START))
        gradient.setColorAt(1.0, QColor(COLOR_BACKGROUND_END))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Menu bar with Akun and Logout action
        menubar = self.menuBar()
        akun_menu = menubar.addMenu("Akun")
        logout_action = QAction("Logout", self)
        akun_menu.addAction(logout_action)
        logout_action.triggered.connect(self.handle_logout)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(24)
        
        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setSpacing(24)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container.setLayout(container_layout)
        container.setMaximumWidth(900)
        # Assuming ShadowedTitle is defined elsewhere, otherwise fallback to QLabel with bold style
        try:
            title_widget = ShadowedTitle("Kuis: Gerak Lurus")
        except NameError:
            title_widget = QLabel("Kuis: Gerak Lurus")
            title_widget.setFont(QFont("Inter", 48, QFont.Bold))
            title_widget.setStyleSheet("color: #111827;")
        container_layout.addWidget(title_widget, alignment=Qt.AlignHCenter)
        
        main_layout.addWidget(container, alignment=Qt.AlignCenter)

        # Text area container styled as a card with subtle rounded corners and background
        self.text_area_container = QFrame()
        self.text_area_container.setStyleSheet("""
            QFrame {
                border: 2px solid #374151;
                border-radius: 12px;
                background-color: #cbd5e1;
            }
        """)
        self.text_area_container.setMinimumHeight(96)
        self.text_area_container.setLayout(QHBoxLayout())
        self.text_area_container.layout().setContentsMargins(48, 12, 12, 12)
        self.text_area_container.layout().setSpacing(0)

        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                border: none;
                font-size: 16px;
                color: black;
                padding-left: 0px;
                resize: none;
            }
        """)
        self.text_edit.setFixedHeight(72)
        self.text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.text_edit.setReadOnly(True)
        self.text_area_container.layout().addWidget(self.text_edit)

        self.number_circle = QLabel("1", self.text_area_container)
        self.number_circle.setFixedSize(40, 40)
        self.number_circle.setAlignment(Qt.AlignCenter)
        self.number_circle.setStyleSheet("""
            background-color: #a9a9a9;
            border-radius: 20px;
            font-weight: bold;
            font-size: 16px;
            color: black;
        """)
        self.number_circle.move(8, 8)
        self.number_circle.raise_()

        main_layout.addWidget(self.text_area_container)

        # Buttons for choices
        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.setSpacing(16)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)

        self.choice_buttons = []
        for i in range(1, 5):
            btn = QPushButton(f"Pilihan {i}")
            btn.setFont(QFont("Sans Serif", 14, QFont.ExtraBold))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #cbd5e1;
                    border: 2px solid #374151;
                    border-radius: 20px;
                    color: black;
                    padding: 10px 0;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #94a3b8;
                }
            """)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setMinimumHeight(40)
            btn.clicked.connect(lambda checked, b=btn: self.check_answer(b))
            self.buttons_layout.addWidget(btn)
            self.choice_buttons.append(btn)

        buttons_container = QWidget()
        buttons_container.setLayout(self.buttons_layout)
        buttons_container.setMaximumWidth(320)
        buttons_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        main_layout.addWidget(buttons_container, alignment=Qt.AlignCenter)

        # Next button styled according to DEFAULT design
        self.next_button = QPushButton("Next", self)
        self.next_button.setFont(QFont("Sans Serif", 14, QFont.ExtraBold))
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_BUTTON_START}, stop:1 {COLOR_BUTTON_END});
                color: white;
                font-size: 18px;
                border: none;
                border-radius: 20px;
                color: white;
                padding: 12px;
                font-weight: bold;
                min-width: 100px;
                min-height: 40px;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        self.next_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.next_button.clicked.connect(self.next_question)
        main_layout.addWidget(self.next_button, alignment=Qt.AlignCenter)
        self.next_button.hide()

        # Menu button styled exactly like Next button
        self.menu_button = QPushButton("Menu", self)
        self.menu_button.setFont(QFont("Sans Serif", 14, QFont.ExtraBold))
        self.menu_button.setStyleSheet(self.next_button.styleSheet())
        self.menu_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.menu_button.clicked.connect(self.back_to_menu)
        main_layout.addWidget(self.menu_button, alignment=Qt.AlignCenter)
        self.menu_button.hide()

        # Load questions from CSV
        self.questions = self.load_questions('source/soal.csv')
        self.current_question_index = 0
        self.display_question()

    def load_questions(self, file_path):
        questions = []
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                questions.append(row)
        return questions

    def display_question(self):
        question = self.questions[self.current_question_index]
        self.text_edit.setPlainText(question['soal'])
        self.number_circle.setText(str(self.current_question_index + 1))
        self.choice_buttons[0].setText(question['a'])
        self.choice_buttons[1].setText(question['b'])
        self.choice_buttons[2].setText(question['c'])
        self.choice_buttons[3].setText(question['d'])

        # When displaying a question reset buttons
        for btn in self.choice_buttons:
            btn.setEnabled(True)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #cbd5e1;
                    border: 2px solid #374151;
                    border-radius: 20px;
                    color: black;
                    padding: 10px 0;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #94a3b8;
                }
            """)

        # Hide both navigation buttons until user answers
        self.next_button.hide()
        self.menu_button.hide()

    def check_answer(self, selected_button):
        # Disable buttons to lock answer
        for btn in self.choice_buttons:
            btn.setEnabled(False)

        question = self.questions[self.current_question_index]
        correct_answer_text = question.get('correct', '').strip()
        selected_text = selected_button.text()

        # Highlight buttons according to correctness
        for btn in self.choice_buttons:
            if btn.text() == correct_answer_text:
                # Correct answer style - green
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #34d399;
                        border: 2px solid #059669;
                        border-radius: 20px;
                        color: white;
                        padding: 10px 0;
                        min-width: 80px;
                    }
                """)
            elif btn == selected_button:
                # Wrong answer style - red
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #f87171;
                        border: 2px solid #dc2626;
                        border-radius: 20px;
                        color: white;
                        padding: 10px 0;
                        min-width: 80px;
                    }
                """)
            else:
                # Other buttons dimmed
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #cbd5e1;
                        border: 2px solid #374151;
                        border-radius: 20px;
                        color: black;
                        padding: 10px 0;
                        opacity: 0.6;
                        min-width: 80px;
                    }
                """)

        # Show next or menu button after answer
        if self.current_question_index < len(self.questions) - 1:
            self.next_button.show()
            self.menu_button.hide()
        else:
            self.next_button.hide()
            self.menu_button.show()

    def next_question(self):
        self.current_question_index += 1
        self.display_question()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        margin = 32
        pass

    def back_to_menu(self):
        self.menu_window.menu_window.show()
        self.close()

    def handle_logout(self):
        self.menu_window.login_window.show()
        self.menu_window.close()
        self.close()

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    login_window = Login()
    login_window.show()
    sys.exit(app.exec_())

