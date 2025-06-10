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
    """
    Main menu screen allowing navigation to different material sections.
    Dynamically sizes itself based on screen resolution.
    """
    def __init__(self, login_window):
        super(Menu, self).__init__()
        self.login_window = login_window
        self.setWindowTitle("PhySim - Menu")

        # Get primary screen geometry for initial sizing
        screen_rect = QApplication.primaryScreen().geometry()
        initial_width = int(screen_rect.width() * 0.7) # 70% of screen width
        initial_height = int(screen_rect.height() * 0.7) # 70% of screen height
        self.resize(initial_width, initial_height)
        self.setMinimumSize(int(initial_width * 0.6), int(initial_height * 0.6)) # Set a flexible minimum size

        # Menu bar - adjust font sizes
        menubar = self.menuBar()
        menubar.setStyleSheet(f"""
            QMenuBar {{
                background-color: #f9f9f9;
                font-weight: 600;
                font-size: {int(1.2 * QApplication.font().pointSize())}px;
                color: #111111;
            }}
            QMenuBar::item {{
                spacing: {int(0.5 * QApplication.font().pointSize())}px;
                padding: {int(0.5 * QApplication.font().pointSize())}px {int(1.0 * QApplication.font().pointSize())}px;
                background: transparent;
                border-radius: 4px;
            }}
            QMenuBar::item:selected {{
                background: #e2e8f0;
            }}
            QMenu {{
                background-color: #f9f9f9;
                border: 1px solid #ddd;
            }}
            QMenu::item:selected {{
                background-color: #cbd5e1;
                color: #111111;
            }}
        """)
        account_menu = menubar.addMenu("Akun")
        logout_action = QAction("Logout", self)
        account_menu.addAction(logout_action)
        logout_action.triggered.connect(self.handle_logout)

        # Background gradient
        palette = QPalette()
        gradient = QLinearGradient(0, 0, screen_rect.width(), screen_rect.height())
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
        main_layout.addStretch(1) # Add flexible space at the top

        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setSpacing(int(initial_height * 0.04)) # Dynamic spacing
        container_layout.setContentsMargins(0,0,0,0)
        container.setLayout(container_layout)
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) # Allow expansion

        title_widget = ShadowedTitle("Pilih Materi", parent=container) # Pass container as parent
        container_layout.addWidget(title_widget, alignment=Qt.AlignHCenter)
        main_layout.addWidget(container, alignment=Qt.AlignCenter)

        button_grid = QGridLayout()
        # Ensure grid columns are flexible and expand equally
        button_grid.setColumnStretch(0, 1)
        button_grid.setColumnStretch(1, 1)
        button_grid.setColumnStretch(2, 1)

        simulasi_labels = ["Gerak Lurus", "Hukum Newton", "Hukum Hooke", "Rangkaian Resistor", "Gerak Harmonik", "Hukum Archimedes"]

        buttons = [] # Initialize buttons list here

        # Scale icon size and font for menu buttons
        icon_size = int(min(initial_width, initial_height) * 0.12) # Example: 12% of the smaller dimension
        label_font_size = int(1.1 * QApplication.font().pointSize())

        for i in range(6):
            icon_path = f"icons/{i + 1}.png"
            btn = QPushButton()
            btn.setObjectName(f"MenuIcon_{i+1}") # Set unique object name for each menu button
            btn.setFixedSize(icon_size, icon_size) # Fixed size for button/icon
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed) # Fixed size
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
            label.setObjectName(f"MenuLabel_{i+1}") # Set unique object name for each menu label
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(f"color: black; font-weight: bold; font-size: {label_font_size}px;")

            vbox = QVBoxLayout()
            vbox.addStretch() # Add stretch to center button/label vertically
            vbox.addWidget(btn, alignment=Qt.AlignCenter)
            vbox.addWidget(label, alignment=Qt.AlignCenter)
            vbox.addStretch()

            container_item = QWidget() # Rename to avoid conflict with outer container
            container_item.setLayout(vbox)
            container_item.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) # Ensure inner container expands

            button_grid.addWidget(container_item, i // 3, i % 3)

        main_layout.addLayout(button_grid)
        main_layout.addStretch(1) # Add flexible space at the bottom

        # Override resizeEvent for Menu to dynamically adjust button sizes
        self.resizeEvent = self.menu_resizeEvent

    def menu_resizeEvent(self, event):
        """
        Overrides resizeEvent to dynamically adjust button sizes and icon sizes
        in the menu grid when the window size changes.
        """
        super().resizeEvent(event)
        current_width = self.width()
        current_height = self.height()

        # Update shadowed title size
        self.findChild(ShadowedTitle)._update_sizes()

        # Recalculate icon size and label font size
        new_icon_size = int(min(current_width, current_height) * 0.12)
        # Scale font relative to initial height, ensuring it doesn't get too small
        new_label_font_size = max(10, int(1.1 * QApplication.font().pointSize() * (current_height / self.minimumHeight()))) 

        for i in range(6): # Iterate through all 6 menu items
            btn = self.findChild(QPushButton, f"MenuIcon_{i+1}")
            label = self.findChild(QLabel, f"MenuLabel_{i+1}")

            if btn:
                btn.setFixedSize(new_icon_size, new_icon_size)
                # Reapply stylesheet to ensure changes take effect (especially if sizes are part of it)
                btn.setStyleSheet(btn.styleSheet()) 

            if label:
                label.setStyleSheet(f"color: black; font-weight: bold; font-size: {new_label_font_size}px;")


    def open_screen(self, index):
        """Opens the selected material screen."""
        self.hide() # Hide menu when opening a new screen
        # Use a dictionary to map index to class for better scalability
        material_screens_map = {
            0: GL,
            1: Newton,
            2: Hooke,
            3: Resistor,
            4: Bandul,
            5: Archimedes,
        }
        screen_class = material_screens_map.get(index)
        if screen_class:
            self.screen = screen_class(self)
            self.screen.show()
        else:
            print(f"Error: No screen defined for index {index}")


    def handle_logout(self):
        """Handles logout action from the menu."""
        self.login_window.show()
        self.close()
