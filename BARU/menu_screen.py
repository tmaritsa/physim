# menu_screen.py

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton,
    QAction, QApplication, QSizePolicy
)
from PyQt5.QtGui import QPalette, QLinearGradient, QColor, QBrush, QFont, QPixmap
from PyQt5.QtCore import Qt, QSize

from config import COLOR_BACKGROUND_START, COLOR_BACKGROUND_END
from widgets import ShadowedTitle
# Import material screens here to prevent circular import if GL needs Menu
from material_screens import GL, Newton, Hooke, Resistor, Bandul, Archimedes

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
