from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton,
    QAction, QApplication, QSizePolicy, QSpacerItem
)
from PyQt5.QtGui import QPalette, QLinearGradient, QColor, QBrush, QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize

from config import COLOR_BACKGROUND_START, COLOR_BACKGROUND_END
from widgets import ShadowedTitle
from material_screens import GL, Newton, Hooke, Resistor, Bandul, Archimedes

class Menu(QMainWindow):
    def __init__(self, login_window):
        super(Menu, self).__init__()
        self.login_window = login_window
        self.setWindowTitle("PhySim - Menu")
        self.setWindowIcon(QIcon('icons/atom.png'))
        self.resize(800, 600)

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

        palette = QPalette()
        gradient = QLinearGradient(0, 0, 800, 600)
        gradient.setColorAt(0.0, QColor(COLOR_BACKGROUND_START))
        gradient.setColorAt(1.0, QColor(COLOR_BACKGROUND_END))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

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
        button_grid.setSpacing(20)
        button_grid.setContentsMargins(0, 0, 0, 0)
        
        for col in range(3):
            button_grid.setColumnStretch(col, 1)
        for row in range(2):
            button_grid.setRowStretch(row, 1)

        simulasi_labels = ["Gerak Lurus", "Hukum Newton", "Hukum Hooke", "Rangkaian Resistor", "Gerak Harmonik", "Hukum Archimedes"]

        for i in range(6):
            btn = QPushButton()
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border: 1px solid #aaa;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    border-color: #0078d4;
                    box-shadow: 0 0 8px rgba(0,120,212,0.6);
                }
            """)
            btn.clicked.connect(lambda checked, index=i: self.open_screen(index))

            btn_layout = QVBoxLayout(btn)
            btn_layout.setContentsMargins(8, 8, 8, 8)
            btn_layout.setSpacing(4)

            icon_path = f"icons/{i + 1}.png"
            pixmap = QPixmap(icon_path)
            
            icon_label = QLabel()
            icon_label.setPixmap(pixmap)
            icon_label.setAlignment(Qt.AlignCenter)
            
            icon_label.setScaledContents(True)
            icon_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            icon_label.setMinimumSize(40, 40)

            text_label = QLabel(simulasi_labels[i])
            text_label.setAlignment(Qt.AlignCenter)
            text_label.setStyleSheet("color: black; font-weight: bold; font-size: 14px;")
            text_label.setWordWrap(True)

            btn_layout.addWidget(icon_label, stretch=3)
            btn_layout.addWidget(text_label, stretch=1)
            
            btn.setMinimumHeight(120)

            button_grid.addWidget(btn, i // 3, i % 3)

        main_layout.addStretch(1)
        main_layout.addLayout(button_grid)
        main_layout.addStretch(1)
        
        central_widget.setContentsMargins(20, 20, 20, 20)

    def open_screen(self, index):
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