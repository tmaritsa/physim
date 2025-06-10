# material_screens.py

import pygame
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QAction, QApplication, QSizePolicy, QFrame, QSlider, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QPalette, QLinearGradient, QColor, QBrush, QFont
from PyQt5.QtCore import Qt, QTimer

from config import COLOR_BACKGROUND_START, COLOR_BACKGROUND_END, COLOR_BUTTON_START, COLOR_BUTTON_END
from widgets import ShadowedTitle, PygameEmbedWidget
from glbb import GLBBSimulation # Import the simulation logic

# Late import for Kuis to avoid circular dependency, as Kuis also imports Materi
# and Materi (specifically GL) might need Kuis.
# This import will be done inside the gokuis method.

class Materi(QMainWindow):
    """
    Base class for material screens.
    Dynamically sizes itself based on screen resolution.
    """
    def __init__(self, menu_window, title):
        super(Materi, self).__init__()
        self.menu_window = menu_window
        self.setWindowTitle(title)

        # Get primary screen geometry for initial sizing
        screen_rect = QApplication.primaryScreen().geometry()
        initial_width = int(screen_rect.width() * 0.8) # 80% of screen width
        initial_height = int(screen_rect.height() * 0.8) # 80% of screen height
        self.resize(initial_width, initial_height)
        self.setMinimumSize(int(initial_width * 0.6), int(initial_height * 0.6)) # Set a flexible minimum size

        # Background gradient
        palette = QPalette()
        gradient = QLinearGradient(0, 0, screen_rect.width(), screen_rect.height()) # Use screen_rect for gradient
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
        # Dynamic margins based on initial window size
        self.main_layout.setContentsMargins(int(initial_width * 0.05), int(initial_height * 0.05), int(initial_width * 0.05), int(initial_height * 0.05))
        self.main_layout.setSpacing(0)

        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setSpacing(0)
        container_layout.setContentsMargins(0,0,0,0)
        container.setLayout(container_layout)
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) # Allow container to expand horizontally

        title_widget = ShadowedTitle(title, parent=container) # Pass container as parent
        container_layout.addWidget(title_widget, alignment=Qt.AlignHCenter)
        self.main_layout.addWidget(container, alignment=Qt.AlignCenter)

        # Content label that subclasses can customize
        self.content_label = QLabel()
        # Scale font size based on default font
        self.content_label.setStyleSheet(f"color: #6b7280; font-size: {int(1.5 * QApplication.font().pointSize())}px; line-height: 1.4;")
        self.content_label.setAlignment(Qt.AlignCenter)
        self.content_label.setWordWrap(True)
        self.main_layout.addWidget(self.content_label, alignment=Qt.AlignTop)

        # Spacer frame (flexible space)
        spacer = QFrame()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_layout.addWidget(spacer)

        # Menu bar (sticky) - already adaptive, but adjust font sizes
        self.menu_bar = self.menuBar()
        self.menu_bar.setStyleSheet(f"""
            QMenuBar {{
                background-color: #ffffff;
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

        account_menu = self.menu_bar.addMenu("Akun")
        logout_action = QAction("Logout", self)
        account_menu.addAction(logout_action)
        logout_action.triggered.connect(self.logout)

    def _set_content_text(self, text: str):
        """Sets the text content of the material screen."""
        self.content_label.setText(text)

    def back_to_menu(self):
        """Returns to the main menu."""
        self.menu_window.show()
        self.close()

    def logout(self):
        """Handles logout action, returning to the login screen."""
        # Access login_window through menu_window.login_window
        self.menu_window.login_window.show()
        self.menu_window.close()  # Close menu window
        self.close()

    def resizeEvent(self, event):
        """Handle resize events to update sizes of elements in Materi screen."""
        super().resizeEvent(event)
        # Update shadowed title size (handled by its own resizeEvent if parent is set correctly)
        self.findChild(ShadowedTitle)._update_sizes()


class GL(Materi):
    """
    Gerak Lurus (Straight Motion) material screen with simulation.
    Elements dynamically resize with the window.
    """
    def __init__(self, menu_window):
        super(GL, self).__init__(menu_window, "Gerak Lurus")

        # Get current window size (after super() init sets initial size)
        current_width = self.centralWidget().width()
        current_height = self.centralWidget().height()

        # Scale Pygame window based on available space, maintaining aspect ratio
        pygame_display_width = int(current_width * 0.95) # Target 95% of available width
        pygame_display_height = int(pygame_display_width * (400 / 800)) # Maintain 2:1 aspect ratio

        # Ensure minimum size for pygame display
        min_pygame_width = 300
        min_pygame_height = 150
        pygame_display_width = max(min_pygame_width, pygame_display_width)
        pygame_display_height = max(min_pygame_height, pygame_display_height)


        self.simulation = GLBBSimulation(width=pygame_display_width, height=pygame_display_height)
        self.pygame_widget = PygameEmbedWidget(self.simulation) # No fixed size here
        # Set initial fixed size for pygame widget, will be adjusted by resizeEvent
        self.pygame_widget.setFixedSize(pygame_display_width, pygame_display_height)


        # self.kuis_screen is now initialized in gokuis to prevent circular import.
        # It's better not to create it here directly.


        # Wrap pygame_widget in horizontal layout to center and raise its vertical position
        hbox_sim = QHBoxLayout()
        hbox_sim.addStretch()
        hbox_sim.addWidget(self.pygame_widget)
        hbox_sim.addStretch()

        container_sim = QWidget()
        vbox_container = QVBoxLayout()
        vbox_container.setContentsMargins(0, 0, 0, 0)
        vbox_container.addLayout(hbox_sim)
        container_sim.setLayout(vbox_container)
        container_sim.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) # Allow expansion
        self.main_layout.addWidget(container_sim)

        # Scale font size based on default font
        self.slider_label = QLabel("Akselerasi: 0.00 m/s²")
        self.slider_label.setAlignment(Qt.AlignCenter)
        self.slider_label.setFont(QFont("Arial", int(1.2 * QApplication.font().pointSize())))
        self.main_layout.addWidget(self.slider_label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(-5000, 5000)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.update_acceleration)
        self.slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) # Allow width to expand, height fixed
        # Set initial width for slider, will be adjusted by resizeEvent
        self.slider.setFixedWidth(pygame_display_width) # Match initial width to pygame display

        # Put slider inside horizontal layout for centered expansion
        slider_layout = QHBoxLayout()
        slider_layout.setContentsMargins(0, 0, 0, 0)
        slider_layout.addStretch()
        slider_layout.addWidget(self.slider)
        slider_layout.addStretch()
        self.main_layout.addLayout(slider_layout)

        # Buttons for Menu and Kuis in layout constrained by max width
        button_layout = QHBoxLayout()
        button_layout.setSpacing(int(current_width * 0.02)) # Dynamic spacing

        # Scale button padding and font dynamically
        button_font_size = int(1.5 * QApplication.font().pointSize())
        button_padding_v = int(1.0 * QApplication.font().pointSize())
        button_padding_h = int(2.0 * QApplication.font().pointSize())

        back_btn = QPushButton("Menu")
        back_btn.setObjectName("MenuButton") # Set object name
        back_btn.setStyleSheet(f"""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_BUTTON_START}, stop:1 {COLOR_BUTTON_END});
            color: white;
            padding: {button_padding_v}px {button_padding_h}px;
            font-size: {button_font_size}px;
            font-weight: bold;
            border: none;
            border-radius: 20px;
        """)
        back_btn.clicked.connect(self.back_to_menu)
        back_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) # Allow horizontal expansion
        button_layout.addWidget(back_btn)

        kuis_btn = QPushButton("Kuis")
        kuis_btn.setObjectName("KuisButton") # Set object name
        kuis_btn.setStyleSheet(f"""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_BUTTON_START}, stop:1 {COLOR_BUTTON_END});
            color: white;
            padding: {button_padding_v}px {button_padding_h}px;
            font-size: {button_font_size}px;
            font-weight: bold;
            border: none;
            border-radius: 20px;
        """)
        kuis_btn.clicked.connect(self.gokuis)
        kuis_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) # Allow horizontal expansion
        button_layout.addWidget(kuis_btn)

        button_layout.addStretch()

        button_container = QWidget()
        button_container.setLayout(button_layout)
        button_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) # Allow container to expand horizontally
        self.main_layout.addWidget(button_container, alignment=Qt.AlignCenter)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.game_tick)
        self.timer.start(1000 // 60)

    def gokuis(self):
        """Switches to the Kuis (Quiz) screen."""
        from quiz_screen import Kuis # Late import for Kuis to break circular dependency
        self.kuis_screen = Kuis(self) # Initialize Kuis here, not in __init__
        self.kuis_screen.show()
        self.close()

    def update_acceleration(self, value):
        """Updates the simulation's acceleration based on slider value."""
        accel_value = value / 100.0
        self.simulation.set_acceleration(accel_value)
        self.slider_label.setText(f"Akselerasi: {accel_value:.2f} m/s²")

    def game_tick(self):
        """Updates the simulation state and redraws the Pygame widget."""
        self.simulation.step()
        self.simulation.draw()
        self.pygame_widget.update_display()

    def resizeEvent(self, event):
        """
        Overrides resizeEvent to dynamically resize Pygame simulation and slider
        when the window size changes.
        """
        super().resizeEvent(event)
        # Get the current width of the central widget's content area
        current_width = self.centralWidget().width()
        current_height = self.centralWidget().height()

        # Update shadowed title size
        self.findChild(ShadowedTitle)._update_sizes()

        # Recalculate pygame widget size based on new central widget size
        main_layout_margins_h = self.main_layout.contentsMargins().left() + self.main_layout.contentsMargins().right()
        available_width_for_sim = current_width - main_layout_margins_h

        pygame_target_width = int(available_width_for_sim * 0.95) # Target 95% of available horizontal space
        pygame_target_height = int(pygame_target_width * (400 / 800)) # Maintain 2:1 aspect ratio

        # Define minimum sizes to prevent elements from becoming too small
        min_pygame_width = 300
        min_pygame_height = 150

        final_pygame_width = max(min_pygame_width, pygame_target_width)
        final_pygame_height = max(min_pygame_height, pygame_target_height)

        self.pygame_widget.setFixedSize(final_pygame_width, final_pygame_height)
        self.simulation.resize(final_pygame_width, final_pygame_height) # Resize the internal pygame surface

        # Adjust slider width to match pygame simulation width
        self.slider.setFixedWidth(final_pygame_width)

        # Update button font sizes and padding on resize
        # Scale button font relative to current window height for responsiveness
        button_font_size = max(12, int(1.5 * QApplication.font().pointSize() * (current_height / self.minimumHeight()))) 
        button_padding_v = int(1.0 * button_font_size * 0.7)
        button_padding_h = int(2.0 * button_font_size * 0.7)

        # Find buttons by their object names
        menu_btn = self.findChild(QPushButton, "MenuButton")
        kuis_btn = self.findChild(QPushButton, "KuisButton")

        if menu_btn:
            menu_btn.setFont(QFont("Sans Serif", button_font_size, QFont.Bold))
            menu_btn.setStyleSheet(f"""
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_BUTTON_START}, stop:1 {COLOR_BUTTON_END});
                color: white;
                padding: {button_padding_v}px {button_padding_h}px;
                font-size: {button_font_size}px;
                font-weight: bold;
                border: none;
                border-radius: 20px;
            """)
        if kuis_btn:
            kuis_btn.setFont(QFont("Sans Serif", button_font_size, QFont.Bold))
            kuis_btn.setStyleSheet(f"""
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_BUTTON_START}, stop:1 {COLOR_BUTTON_END});
                color: white;
                padding: {button_padding_v}px {button_padding_h}px;
                font-size: {button_font_size}px;
                font-weight: bold;
                border: none;
                border-radius: 20px;
            """)


class Newton(Materi):
    """Newton's Law material screen."""
    def __init__(self, menu_window):
        super(Newton, self).__init__(menu_window, "Hukum Newton")
        self._set_content_text("Penjelasan mengenai hukum Newton akan ditampilkan di sini.")
        back_btn = QPushButton("Menu")
        back_btn.setObjectName("MenuButton_Newton") # Set object name
        # Scale button padding and font dynamically
        button_font_size = int(1.5 * QApplication.font().pointSize())
        button_padding_v = int(1.0 * QApplication.font().pointSize())
        button_padding_h = int(2.0 * QApplication.font().pointSize())
        back_btn.setStyleSheet(f"""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_BUTTON_START}, stop:1 {COLOR_BUTTON_END});
            color: white;
            padding: {button_padding_v}px {button_padding_h}px;
            font-size: {button_font_size}px;
            font-weight: bold;
            border: none;
            border-radius: 20px;
        """)
        back_btn.clicked.connect(self.back_to_menu)
        self.main_layout.addWidget(back_btn, alignment=Qt.AlignCenter) # Center button

class Hooke(Materi):
    """Hooke's Law material screen."""
    def __init__(self, menu_window):
        super(Hooke, self).__init__(menu_window, "Hukum Hooke")
        self._set_content_text("Penjelasan mengenai hukum Hooke akan ditampilkan di sini.")
        back_btn = QPushButton("Menu")
        back_btn.setObjectName("MenuButton_Hooke") # Set object name
        # Scale button padding and font dynamically
        button_font_size = int(1.5 * QApplication.font().pointSize())
        button_padding_v = int(1.0 * QApplication.font().pointSize())
        button_padding_h = int(2.0 * QApplication.font().pointSize())
        back_btn.setStyleSheet(f"""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_BUTTON_START}, stop:1 {COLOR_BUTTON_END});
            color: white;
            padding: {button_padding_v}px {button_padding_h}px;
            font-size: {button_font_size}px;
            font-weight: bold;
            border: none;
            border-radius: 20px;
        """)
        back_btn.clicked.connect(self.back_to_menu)
        self.main_layout.addWidget(back_btn, alignment=Qt.AlignCenter) # Center button


class Resistor(Materi):
    """Resistor Circuit material screen."""
    def __init__(self, menu_window):
        super(Resistor, self).__init__(menu_window, "Rangkaian Resistor")
        self._set_content_text("Simulasi rangkaian resistor akan ditampilkan di sini.")
        back_btn = QPushButton("Menu")
        back_btn.setObjectName("MenuButton_Resistor") # Set object name
        # Scale button padding and font dynamically
        button_font_size = int(1.5 * QApplication.font().pointSize())
        button_padding_v = int(1.0 * QApplication.font().pointSize())
        button_padding_h = int(2.0 * QApplication.font().pointSize())
        back_btn.setStyleSheet(f"""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_BUTTON_START}, stop:1 {COLOR_BUTTON_END});
            color: white;
            padding: {button_padding_v}px {button_padding_h}px;
            font-size: {button_font_size}px;
            font-weight: bold;
            border: none;
            border-radius: 20px;
        """)
        back_btn.clicked.connect(self.back_to_menu)
        self.main_layout.addWidget(back_btn, alignment=Qt.AlignCenter) # Center button


class Bandul(Materi):
    """Simple Harmonic Motion material screen."""
    def __init__(self, menu_window):
        super(Bandul, self).__init__(menu_window, "Gerak Harmonik")
        self._set_content_text("Simulasi gerak harmonik sederhana akan ditampilkan di sini.")
        back_btn = QPushButton("Menu")
        back_btn.setObjectName("MenuButton_Bandul") # Set object name
        # Scale button padding and font dynamically
        button_font_size = int(1.5 * QApplication.font().pointSize())
        button_padding_v = int(1.0 * QApplication.font().pointSize())
        button_padding_h = int(2.0 * QApplication.font().pointSize())
        back_btn.setStyleSheet(f"""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_BUTTON_START}, stop:1 {COLOR_BUTTON_END});
            color: white;
            padding: {button_padding_v}px {button_padding_h}px;
            font-size: {button_font_size}px;
            font-weight: bold;
            border: none;
            border-radius: 20px;
        """)
        back_btn.clicked.connect(self.back_to_menu)
        self.main_layout.addWidget(back_btn, alignment=Qt.AlignCenter) # Center button


class Archimedes(Materi):
    """Archimedes' Principle material screen."""
    def __init__(self, menu_window):
        super(Archimedes, self).__init__(menu_window, "Hukum Archimedes")
        self._set_content_text("Penjelasan tentang hukum Archimedes akan ditampilkan di sini.")
        back_btn = QPushButton("Menu")
        back_btn.setObjectName("MenuButton_Archimedes") # Set object name
        # Scale button padding and font dynamically
        button_font_size = int(1.5 * QApplication.font().pointSize())
        button_padding_v = int(1.0 * QApplication.font().pointSize())
        button_padding_h = int(2.0 * QApplication.font().pointSize())
        back_btn.setStyleSheet(f"""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_BUTTON_START}, stop:1 {COLOR_BUTTON_END});
            color: white;
            padding: {button_padding_v}px {button_padding_h}px;
            font-size: {button_font_size}px;
            font-weight: bold;
            border: none;
            border-radius: 20px;
        """)
        back_btn.clicked.connect(self.back_to_menu)
        self.main_layout.addWidget(back_btn, alignment=Qt.AlignCenter) # Center button
